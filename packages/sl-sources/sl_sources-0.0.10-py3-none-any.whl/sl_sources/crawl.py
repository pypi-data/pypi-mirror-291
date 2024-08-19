import asyncio
import hashlib
import json
import os
import traceback
from typing import Any, Dict, List, Optional, Union

import aiohttp

from .models import (
    ENTITY_MODELS,
    ENTITY_TYPES,
    SOURCE_TYPES,
    WORK_TYPES,
    Author,
    Entity,
    Institution,
    Publication,
    Publisher,
    SearchInput,
    Work,
)

from .http import cloud_function_request, resolve_url, validate_url
from .papers import get_paper_details
from .sources import download_search_result, search_and_download


def read_cache(cache_filename: str) -> Dict[str, Any]:
    """
    Read the cache from a JSON file.
    """
    # Load or create cache
    cache: Dict[str, Any] = {}
    if os.path.exists(cache_filename):
        with open(cache_filename, "r") as f:
            cache = json.load(f)
    return cache


async def update_cache(cache: Dict[str, Any], entity: Entity, filename) -> None:
    """
    Update the cache with a new entity and save to json file.

    Parameters
    ----------
    cache : Dict[str, Any]
        The current cache dictionary.
    entity : Entity
        The entity to add or update in the cache.

    Returns
    -------
    None
    """
    # Generate a unique hash for the entity based on its URL or ID
    url_hash = (
        hashlib.md5(entity.url.encode()).hexdigest()
        if hasattr(entity, "url")
        else entity.id
    )

    # Add or update the entity in the cache
    cache[url_hash] = entity

    # Serialize the cache and write it to JSON file
    with open(filename, "w") as f:
        json.dump(
            {
                k: v.model_dump() if hasattr(v, "model_dump") else v
                for k, v in cache.items()
            },
            f,
            indent=2,
        )


async def _download_and_evaluate(
    source: Work,
    depth: int,
    max_depth: int,
    use_cloud_function: bool,
    semaphore: asyncio.Semaphore,
    research_topic: str,
    entity_types: List[str],
    cache: Dict[str, Any],
    cache_filename: str,
) -> Entity:
    """
    Download and evaluate a single work.

    Parameters
    ----------
    source : Work
        The work to download and evaluate.
    depth : int
        The current depth in the crawl process.
    max_depth : int
        The maximum depth to crawl.
    use_cloud_function : bool
        Whether to use a cloud function for downloading.
    semaphore : asyncio.Semaphore
        Semaphore to control concurrent downloads.
    research_topic : str
        The research topic to evaluate relevance against.
    entity_types : List[str]
        The types of entities to search for.
    cache : Dict[str, Any]
        A dictionary to cache results.

    Returns
    -------
    Entity
        The downloaded and evaluated entity.
    """
    url: str = source.url
    print(f"Starting _download_and_evaluate for {url}")

    try:
        # Validate the URL
        url = validate_url(url)
    except ValueError as e:
        print(f"Skipping invalid URL: {url}. Error: {str(e)}")
        return source

    # Generate a unique hash for the URL
    url_hash: str = hashlib.md5(url.encode()).hexdigest()

    # Check if the URL is already in the cache
    if url_hash in cache:
        print(f"Using cached content for {url}")
        cached_entity = cache[url_hash]
        if isinstance(cached_entity, dict):
            # Convert dict to Work entity if necessary
            return Work(**cached_entity)
        return cached_entity
    else:
        print(f"No cached content for {url}")

    # Use a semaphore to control concurrent downloads
    async with semaphore:
        try:
            print(f"Downloading {url}")
            if use_cloud_function:
                # Use cloud function to download content
                entity_data = await cloud_function_request(
                    "download_search_result",
                    {"search_result": source.model_dump_json()},
                )
                type = entity_data.get("type")
                entity = ENTITY_MODELS[type](**entity_data)
            else:
                # Download search result locally
                print("Downloading search result")
                entity = await download_search_result(source)

            if not entity:
                print(f"No content downloaded for {url}")
                # Create a placeholder Work entity if no content was downloaded
                entity = Work(
                    id=url_hash,
                    url=url,
                    name=f"No content: {url}",
                    abstract="No content downloaded",
                    source_type=SOURCE_TYPES.CRAWL,
                    work_type=WORK_TYPES.UNKNOWN,
                )
                # Update the cache with the placeholder entity
                await update_cache(cache, entity, cache_filename)
                return entity

            # Extract full text based on source type
            if source.source_type == SOURCE_TYPES.YOUTUBE:
                text = entity.full_text if entity.full_text else ""
            else:
                text = entity.full_text if entity.full_text else ""

            print(f"Downloaded content for {url}: {str(text)[:100]}...")

            print(f"Evaluating page for {url}")
            # Evaluate the page content for relevance
            result: Dict[str, Any] = await _evaluate_page(text, research_topic)
            print(f"Evaluation result for {url}: {result}")

            # Create the appropriate entity based on the content type
            if isinstance(entity, Work) and entity.type == ENTITY_TYPES.WORK:
                # rewrite to just add the results to the entity
                entity.abstract = result["abstract"]
                entity.relevant = result["relevant"]
                entity.full_text = text
                entity.links = result["links"]

            # Update the cache with the new entity
            await update_cache(cache, entity, cache_filename)
            print(f"Added to cache: {url}")

            print("result is relevant", result["relevant"])
            if result["relevant"]:
                # If the content is relevant, crawl the links found in the page
                await _crawl_links(
                    result["links"],
                    depth=depth + 1,
                    max_depth=max_depth,
                    cache_filename=cache_filename,
                    parent_source=source,
                    use_cloud_function=use_cloud_function,
                    semaphore=semaphore,
                    research_topic=research_topic,
                    entity_types=entity_types,
                    cache=cache,
                )
            else:
                print(f"Content not relevant: {url}")

            return entity

        except Exception as e:
            print(f"Error downloading/evaluating {url}: {e}")
            print(traceback.format_exc())
            # Create an error Work entity if an exception occurs
            error_entity = Work(
                id=url_hash,
                url=url,
                name=f"Error: {url}",
                abstract=str(e),
                source_type=source.source_type,
                work_type=WORK_TYPES.UNKNOWN,
                authors=[
                    Author(name=author.name, source_type=source.source_type)
                    for author in source.authors
                ],
            )
            # Update the cache with the error entity
            await update_cache(cache, error_entity, cache_filename)
            return error_entity


async def _process_link(
    url: str,
    depth: int,
    max_depth: int,
    source_type: str,
    parent_source: Optional[Dict[str, Any]],
    use_cloud_function: bool,
    semaphore: asyncio.Semaphore,
    research_topic: str,
    entity_types: List[str],
    cache: Dict[str, Any],
    cache_filename,
) -> Optional[Work]:
    """
    Process a single link by getting paper details and evaluating the content.

    Parameters
    ----------
    url : str
        The URL to process.
    depth : int
        The current depth in the crawl process.
    max_depth : int
        The maximum depth to crawl.
    source_type : str
        The type of the source.
    parent_source : Optional[Dict[str, Any]]
        Information about the parent source.
    use_cloud_function : bool
        Whether to use a cloud function for downloading.
    semaphore : asyncio.Semaphore
        Semaphore to control concurrent downloads.
    research_topic : str
        The research topic to evaluate relevance against.
    entity_types : List[str]
        The types of entities to search for.
    cache : Dict[str, Any]
        A dictionary to cache results.

    Returns
    -------
    Optional[Dict[str, Any]]
        A dictionary containing information about the processed link, or None if processing failed.
    """
    print("Processing link")
    # if semaphore is not a semaphore, print an error
    if not isinstance(semaphore, asyncio.Semaphore):
        print("Semaphore is not a semaphore")
        raise ValueError("Semaphore is not a semaphore")

    async with semaphore:
        print("Getting paper details")
        # Attempt to get paper details for the URL
        work: Work = await get_paper_details(url)
        if work is None:
            abstract = f"Crawled from {url}"
            name = "Unkonwn crawled link"
            if parent_source is not None:
                # TODO: if parent source is a dict, use the name and url from the dict
                # This is the case for our tests, but not our actually crawl, so we should remove this
                if isinstance(parent_source, dict):
                    abstract = f"Crawled from {url} with parent {parent_source['name']} | {parent_source['url']}"
                    name = parent_source["name"]
                else:
                    abstract = f"Crawled from {url} with parent {parent_source.name} | {parent_source.url}"
                    name = parent_source.name

            work = Work(
                id=hashlib.md5(url.encode()).hexdigest(),
                work_type=WORK_TYPES.UNKNOWN,
                name=name,
                authors=[],
                abstract=abstract,
                url=url,
                source_type=source_type,
            )

        if work:
            print("work is", work)
            # If work details were successfully retrieved, download and evaluate the content
            result: Entity = await _download_and_evaluate(
                work,
                depth + 1,
                max_depth,
                use_cloud_function,
                semaphore,
                research_topic,
                entity_types,
                cache,
                cache_filename,
            )
            return result
        else:
            print(f"No work found for {url}")
            return None


async def _evaluate_page(
    text: str, research_topic: str, model: str = "gpt-4o-mini"
) -> Dict[str, Any]:
    """
    Evaluate a page's content for relevance to the research topic.

    This function uses OpenAI's API to analyze the text and determine its relevance.

    Parameters
    ----------
    text : str
        The text content of the page to evaluate.
    research_topic : str
        The research topic to evaluate relevance against.
    model : str, optional
        The OpenAI model to use for evaluation (default is "gpt-4o-mini").

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the evaluation results, including relevance,
        extracted links, and an abstract.
    """
    OPENAI_API_KEY: Optional[str] = os.getenv(
        "OPENAI_API_KEY", os.getenv("SOCIETY_API_KEY")
    )
    if not OPENAI_API_KEY:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")

    # Truncate the text if it's too long
    max_length: int = 128000
    if len(text) > max_length:
        text = text[:max_length] + "..."

    # Construct the prompt for the OpenAI API
    prompt: str = f"""
    Analyze the following text and determine if it's relevant. 
    Also extract any URLs mentioned in the text that seem relevant to these topics.
    
    Text:
    {text}
    
    We are researching the following topic and related domains:
    {research_topic}

    Please evaluate if the text above contains relevant and substantive information for our research.

    Respond with a JSON object containing two fields:
    1. "relevant": a boolean indicating if the text is relevant
    2. "links": a list of relevant URLs extracted from the text which are worth looking at. Ignore links that are not relevant to the research topic.
    3. "abstract": a summary of the text, focusing on the most relevant information for the research topic.
    
    Example response:
    {{
        "relevant": true,
        "links": ["https://example.com/ai-article", "https://example.org/ml-study"],
        "abstract": "A summary of the text, focusing on the most relevant information for the research topic."
    }}
    """

    # Make a request to the OpenAI API
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
            },
        ) as response:
            if response.status == 200:
                result: Dict[str, Any] = await response.json()
                try:
                    # Parse the API response
                    evaluation: str = result["choices"][0]["message"]["content"]
                    evaluation = evaluation.replace("```json\n", "").replace(
                        "\n```", ""
                    )
                    evaluation_dict: Dict[str, Any] = json.loads(evaluation)
                    evaluation_dict["text"] = text
                    return evaluation_dict
                except json.JSONDecodeError:
                    print(
                        f"Error parsing GPT-4 response: {result['choices'][0]['message']['content']}"
                    )
                    return {
                        "relevant": False,
                        "links": [],
                        "abstract": "",
                        "text": text,
                    }
            else:
                print(f"Error calling OpenAI API: {response.status}")
                return {"relevant": False, "links": [], "abstract": "", "text": text}


async def _crawl_links(
    links: List[str],
    depth: int,
    max_depth: int,
    cache_filename: str,
    parent_source: Optional[Union[Work, Dict[str, Any]]] = None,
    use_cloud_function: bool = False,
    semaphore: Optional[asyncio.Semaphore] = None,
    research_topic: Optional[str] = None,
    entity_types: Optional[List[str]] = None,
    cache: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Crawl a list of links, processing each one up to a maximum depth.

    Parameters
    ----------
    links : List[str]
        A list of URLs to crawl.
    depth : int
        The current depth in the crawl process.
    max_depth : int
        The maximum depth to crawl.
    parent_source : Optional[Union[Work, Dict[str, Any]]], optional
        Information about the parent source.
    use_cloud_function : bool, optional
        Whether to use a cloud function for downloading.
    semaphore : Optional[asyncio.Semaphore], optional
        Semaphore to control concurrent downloads.
    research_topic : Optional[str], optional
        The research topic to evaluate relevance against.
    entity_types : Optional[List[str]], optional
        The types of entities to search for.
    cache : Optional[Dict[str, Any]], optional
        A dictionary to cache results.

    Returns
    -------
    List[Dict[str, Any]]
        A list of processed link results.
    """
    print("Crawling links")
    if cache is None:
        cache = {}
    if semaphore is None or not isinstance(semaphore, asyncio.Semaphore):
        semaphore = asyncio.Semaphore(10)

    # Determine the source type based on the parent source
    source_type: str = (
        parent_source.source_type
        if isinstance(parent_source, Work)
        else SOURCE_TYPES.CRAWL
    )

    # If we've reached the maximum depth, stop crawling
    if depth > max_depth:
        return []

    tasks: List[asyncio.Task] = []
    for link in links:
        try:
            # Resolve the URL, considering the parent URL if it exists
            resolved_url: str = resolve_url(
                link,
                base_url=parent_source.url if isinstance(parent_source, Work) else None,
            )
            url_hash: str = hashlib.md5(resolved_url.rstrip("/").encode()).hexdigest()

            # If the URL is already in the cache, skip it
            if url_hash in cache:
                print(f"URL {resolved_url} already processed or in cache")
                continue

            # Create a task to process the link
            task: asyncio.Task = asyncio.create_task(
                _process_link(
                    resolved_url,
                    depth,
                    max_depth,
                    source_type=source_type,
                    parent_source=parent_source,
                    use_cloud_function=use_cloud_function,
                    semaphore=semaphore,
                    research_topic=research_topic,
                    entity_types=entity_types,
                    cache=cache,
                    cache_filename=cache_filename,
                )
            )
            tasks.append(task)
        except ValueError as e:
            # If the URL is invalid, log the error and add it to the cache
            print(f"Skipping invalid URL: {link}. Error: {str(e)}")
            cache[hashlib.md5(link.encode()).hexdigest()] = {
                "id": hashlib.md5(link.encode()).hexdigest(),
                "url": link,
                "error": str(e),
                "source_type": source_type,
                "name": "Invalid URL",
                "authors": [],
            }

    # Wait for all tasks to complete
    results: List[Optional[Dict[str, Any]]] = await asyncio.gather(*tasks)
    return [result for result in results if result is not None]


async def _search_and_download_with_semaphore(
    search_input: SearchInput,
    semaphore: asyncio.Semaphore,
    use_cloud_function: bool = False,
) -> List[Entity]:
    """
    Helper function to perform search and download with semaphore control.

    Parameters
    ----------
    search_input : SearchInput
        The search input to use for the search and download.
    semaphore : asyncio.Semaphore
        Semaphore to control concurrent operations.
    use_cloud_function : bool, optional
        Whether to use a cloud function for the operation.

    Returns
    -------
    List[Entity]
        List of search results.
    """
    source_type = search_input.source_type
    query = search_input.query
    entity_types = search_input.entity_types
    num_results = search_input.num_results

    async with semaphore:
        if use_cloud_function:
            # Use cloud function for search and download
            return await cloud_function_request(
                "search_and_download",
                {
                    "source_types": [source_type],
                    "query": query,
                    "num_results": num_results,
                    "entity_types": entity_types,
                },
            )
        else:
            # Perform local search and download
            return await search_and_download(search_input)


async def crawl(
    keywords: List[str] = [],
    urls: List[str] = [],
    source_types: List[str] = [SOURCE_TYPES.OPENALEX, SOURCE_TYPES.GOOGLE_SCHOLAR],
    research_topic: str = "",
    max_depth: int = 3,
    use_cloud_function: bool = False,
    entity_types: List[str] = [
        ENTITY_TYPES.WORK,
        ENTITY_TYPES.AUTHOR,
        ENTITY_TYPES.INSTITUTION,
        ENTITY_TYPES.PUBLICATION,
    ],
    semaphore: asyncio.Semaphore = asyncio.Semaphore(50),
    num_results: int = 5,
    cache_filename: str = "manifest.json",
) -> List[Entity]:
    """
    Main crawling function that processes keywords and URLs from various sources.

    Parameters
    ----------
    keywords : List[str], optional
        List of keywords to search for.
    urls : List[str], optional
        List of URLs to crawl.
    source_types : List[str], optional
        List of sources to use for searching (default is OpenAlex and Google Scholar).
    research_topic : str, optional
        The main research topic.
    max_depth : int, optional
        Maximum depth for crawling (default is 3).
    use_cloud_function : bool, optional
        Whether to use a cloud function for downloading (default is False).
    entity_types : List[str], optional
        Types of entities to search for.
    semaphore : asyncio.Semaphore, optional
        Semaphore to control concurrent downloads (default is 50).
    num_results : int, optional
        Number of results to fetch per search (default is 5).

    Returns
    -------
    List[Entity]
        A list of crawled and processed entities.
    """
    print(f"Crawling with {len(keywords)} keywords and {len(urls)} URLs")

    # Validate and deduplicate URLs
    validated_urls: List[str] = []
    for url in urls:
        try:
            validated_url = validate_url(url)
            validated_urls.append(validated_url)
        except ValueError as e:
            print(f"Skipping invalid URL: {url}. Error: {str(e)}")
            continue

    urls: set = set(validated_urls)
    keywords: set = set(keywords)

    # Normalize and categorize URLs
    arxiv_urls: List[str] = [url for url in urls if "arxiv.org/" in url]
    pubmed_urls: List[str] = [url for url in urls if "pubmed.ncbi.nlm.nih.gov/" in url]
    youtube_urls: List[str] = [url for url in urls if "youtube.com/" in url]
    vimeo_urls: List[str] = [url for url in urls if "vimeo.com/" in url]
    doi_urls: List[str] = [url for url in urls if "doi.org/" in url]

    # Remove categorized URLs from the main list
    urls = [
        url
        for url in urls
        if "arxiv.org" not in url
        and "pubmed.ncbi.nlm.nih.gov/" not in url
        and "youtube.com/" not in url
        and "vimeo.com/" not in url
        and "doi.org/" not in url
    ]

    url_sources: List[Work] = []

    # Create Work objects for each type of URL
    for url in doi_urls:
        id: str = url.split("doi.org/")[1]
        url_sources.append(
            Work(
                id=id,
                name=f"DOI: {id}",
                url=f"https://doi.org/{id}",
                source_type=SOURCE_TYPES.DOI,
                work_type=WORK_TYPES.PAPER,
            )
        )
    for url in arxiv_urls:
        id: str = url.split("/")[-1]
        url_sources.append(
            Work(
                id=id,
                name=f"arXiv: {id}",
                url=url,
                source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,
                work_type=WORK_TYPES.PAPER,
            )
        )
    for url in pubmed_urls:
        id: str = url.split("/")[-1]
        url_sources.append(
            Work(
                id=id,
                name=f"PubMed: {id}",
                url=url,
                source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,
                work_type=WORK_TYPES.PAPER,
            )
        )
    for url in youtube_urls:
        id: str = url.split("v=")[-1].split("&")[0]
        url_sources.append(
            Work(
                id=id,
                name=f"YouTube: {id}",
                url=f"https://www.youtube.com/watch?v={id}",
                source_type=SOURCE_TYPES.YOUTUBE,
                work_type=WORK_TYPES.VIDEO,
            )
        )
    for url in vimeo_urls:
        id: str = url.split("vimeo.com/")[1].split("?")[0]
        url_sources.append(
            Work(
                id=id,
                name=f"Vimeo: {id}",
                url=url,
                source_type="vimeo",
                work_type=WORK_TYPES.VIDEO,
            )
        )

    # Deduplicate URLs
    urls: set = set(urls)

    search_tasks: List[asyncio.Task] = []

    # Create search tasks for each source and keyword combination
    for source_type in source_types:
        for keyword in keywords:
            print(
                f"Searching and downloading for {keyword} with source_type {source_type}"
            )
            task: asyncio.Task = asyncio.create_task(
                _search_and_download_with_semaphore(
                    SearchInput(
                        entity_types=[
                            ENTITY_TYPES.WORK,
                            ENTITY_TYPES.AUTHOR,
                            ENTITY_TYPES.INSTITUTION,
                            ENTITY_TYPES.PUBLICATION,
                        ],
                        query=keyword,
                        num_results=num_results,
                        source_type=source_type,
                    ),
                    semaphore,
                    use_cloud_function,
                )
            )
            search_tasks.append(task)

    # Wait for all search tasks to complete
    search_results: List[List[Any]] = await asyncio.gather(*search_tasks)
    sources: List[Any] = [
        item for sublist in search_results for item in sublist if sublist
    ]
    sources = url_sources + sources

    cache = read_cache(cache_filename)

    # Convert cached items to appropriate entities
    for key, value in cache.items():
        if isinstance(value, dict):
            if value.get("type") == "work":
                cache[key] = Work(**value)
            elif value.get("type") == "author":
                cache[key] = Author(**value)
            elif value.get("type") == "institution":
                cache[key] = Institution(**value)
            elif value.get("type") == "publication":
                cache[key] = Publication(**value)
            elif value.get("type") == "publisher":
                cache[key] = Publisher(**value)

    download_tasks: List[asyncio.Task] = []
    cached_sources: List[Any] = []
    non_work_sources: List[Any] = []
    for source in sources:
        if not isinstance(source, Work):
            print(f"Skipping non-Work source: {source}")
            non_work_sources.append(source)
            continue
        url: str = validate_url(source.url)
        url_hash: str = hashlib.md5(url.encode()).hexdigest()
        if url_hash not in cache:
            task: asyncio.Task = asyncio.create_task(
                _download_and_evaluate(
                    source,
                    0,
                    max_depth,
                    use_cloud_function,
                    semaphore,
                    research_topic,
                    entity_types,
                    cache,
                    cache_filename,
                )
            )
            download_tasks.append(task)
        else:
            print(f"URL {url} already in cache, skipping download")
            cached_sources.append(source)

    # Wait for all download tasks to complete
    results = await asyncio.gather(*download_tasks)

    results = non_work_sources + results + cached_sources

    # Filter None results
    results = [result for result in results if result is not None]

    # Flatten the results and convert to entities
    flattened_results: List[Entity] = []
    for result in results:
        if isinstance(result, list):
            for item in result:
                flattened_results.append(item)
        else:
            flattened_results.append(result)

    print(
        f"Crawl completed. Check the 'downloaded_data' directory {cache_filename} and for results."
    )

    return flattened_results
