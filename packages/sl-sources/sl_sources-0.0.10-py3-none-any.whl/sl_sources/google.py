import asyncio
import hashlib
import json
import os
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
import aiohttp

from .models import SOURCE_TYPES, Work, SearchInput, Entity
from .scrape import browser_scrape

# Load environment variables from .env file
load_dotenv()

# Get Google Search API credentials from environment variables
GOOGLE_SEARCH_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
CSE_ID: Optional[str] = os.getenv("GOOGLE_CSE_ID")


async def search_google(search_input: SearchInput) -> List[Work]:
    """
    Perform a Google search using the Custom Search JSON API.

    This function sends a request to the Google Custom Search API with the
    provided search parameters and processes the results into Work objects.

    Parameters
    ----------
    search_input : SearchInput
        An object containing search parameters including query, number of results,
        and optional file type filter.

    Returns
    -------
    List[Work]
        A list of Work objects representing the search results.

    Notes
    -----
    This function requires valid Google Search API credentials (API key and
    Custom Search Engine ID) to be set as environment variables.
    """
    results: List[Work] = []
    google_api_url: str = "https://customsearch.googleapis.com/customsearch/v1"

    # Prepare parameters for the API request
    params: Dict[str, Any] = {
        "key": GOOGLE_SEARCH_API_KEY,
        "cx": CSE_ID,
        "q": search_input.query,
        "num": search_input.num_results,
    }

    # Add file type filter if specified
    if search_input.file_type:
        params["fileType"] = search_input.file_type

    # Send request to Google Custom Search API
    async with aiohttp.ClientSession() as session:
        async with session.get(google_api_url, params=params) as response:
            response_json: Dict[str, Any] = await response.json()

    # Process search results if any are returned
    if "items" in response_json:
        for item in response_json["items"]:
            url: str = item.get("link", "")
            # Create a unique ID for the work based on its URL
            id: str = hashlib.md5(url.encode()).hexdigest()
            # Create a Work object for each search result
            work = Work(
                id=id,
                name=item.get("title", ""),
                url=url,
                abstract=item.get("snippet", ""),
                full_text="",
                authors=[],
                institutions=[],
                publications=[],
                source_type=SOURCE_TYPES.GOOGLE,
            )
            results.append(work)

    return results


async def download_from_google_search(work: Work) -> Work:
    """
    Download and extract the full text content for a given Work object.

    This function attempts to scrape the full text content from the URL
    associated with the Work object using the browser_scrape function.

    Parameters
    ----------
    work : Work
        A Work object containing at least a URL to scrape.

    Returns
    -------
    Work
        The same Work object, but with the full_text field populated if
        scraping was successful.

    Notes
    -----
    If an error occurs during scraping, it is caught and printed, and the
    original Work object is returned without modification.
    """
    try:
        # Attempt to scrape the full text content from the work's URL
        work.full_text = await browser_scrape(work.url)
        return work
    except Exception as e:
        # If an error occurs, print it and return the original work object
        print(f"Error scraping {work.url}: {e}")
        return work


async def search_and_download_from_google(search_input: SearchInput) -> List[Entity]:
    """
    Perform a Google search and download full text content for the results.

    This function combines the search_google and download_from_google_search
    functions to provide a complete search and download pipeline.

    Parameters
    ----------
    search_input : SearchInput
        An object containing search parameters including query, number of results,
        and optional file type filter.

    Returns
    -------
    List[Entity]
        A list of Entity objects (in this case, Work objects) with full text content.

    Notes
    -----
    This function first performs a search, then attempts to download and extract
    the full text for each search result.
    """
    # Perform the initial search
    search_results: List[Work] = await search_google(search_input)
    entities: List[Entity] = []

    # Download full text for each search result
    for result in search_results:
        downloaded_result: Work = await download_from_google_search(result)
        entities.append(downloaded_result)

    return entities
