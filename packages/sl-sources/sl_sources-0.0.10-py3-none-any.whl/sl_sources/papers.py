import re
from typing import Dict, Any, List, Optional
import aiohttp
from bs4 import BeautifulSoup

from sl_sources.models import SOURCE_TYPES, Work


async def get_paper_details(url: str) -> Work:
    """
    Get paper details from a given URL.

    This function determines the source of the paper (arXiv or PubMed) based on the URL
    and calls the appropriate function to fetch the details.

    Parameters
    ----------
    url : str
        The URL of the paper.

    Returns
    -------
    Work
        A Work object containing the paper details.

    Raises
    ------
    ValueError
        If the URL is not supported (neither arXiv nor PubMed).

    Notes
    -----
    This function serves as a router to direct requests to the appropriate
    paper detail fetching function based on the URL structure.
    """
    if "arxiv.org" in url:
        print("Getting arxiv details")
        return await get_arxiv_details(url)
    elif "pubmed.ncbi.nlm.nih.gov" in url:
        print("Getting pubmed details")
        return await get_pubmed_details(url)
    else:
        return None


async def get_arxiv_details(url: str) -> Work:
    """
    Get paper details from an arXiv URL.

    This function extracts the arXiv ID from the URL, queries the arXiv API,
    and parses the response to extract relevant paper details.

    Parameters
    ----------
    url : str
        The arXiv URL of the paper.

    Returns
    -------
    Work
        A Work object containing the paper details (id, name, authors, abstract).

    Notes
    -----
    This function uses the arXiv API to fetch paper details and BeautifulSoup
    to parse the XML response.
    """
    # Extract arXiv ID from the URL
    arxiv_id: str = re.search(r"(?:arxiv\.org/abs/)(.+)", url).group(1)
    api_url: str = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            # Parse the XML response using BeautifulSoup
            soup = BeautifulSoup(await response.text(), "lxml-xml")

            entry = soup.find("entry")
            name: str = entry.find("name").text
            authors: List[str] = [
                author.find("name").text for author in entry.find_all("author")
            ]
            abstract: str = entry.find("summary").text

            work = Work(
                id=arxiv_id,
                name=name,
                authors=authors,
                abstract=abstract,
                source_type=SOURCE_TYPES.OPENALEX,  # TODO
                doi=f"10.48550/arXiv.{arxiv_id}",
            )

            return work


async def get_pubmed_details(url: str) -> Dict[str, Any]:
    """
    Get paper details from a PubMed URL.

    This function extracts the PubMed ID from the URL, queries the PubMed API
    for both summary and abstract data, and combines the results.

    Parameters
    ----------
    url : str
        The PubMed URL of the paper.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the paper details (id, name, authors, abstract).

    Notes
    -----
    This function uses two separate PubMed API endpoints: one for the summary
    (which includes authors) and another for the abstract.
    """
    # Extract PubMed ID from the URL
    pubmed_id: str = re.search(r"(?:pubmed\.ncbi\.nlm\.nih\.gov/)(\d+)", url).group(1)
    summary_url: str = (
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pubmed_id}&retmode=json"
    )
    abstract_url: str = (
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pubmed_id}&retmode=xml"
    )

    async with aiohttp.ClientSession() as session:
        # Fetch summary data (includes authors)
        async with session.get(summary_url) as response:
            summary_data: Dict[str, Any] = await response.json()
            result = summary_data["result"][pubmed_id]

        # Fetch abstract data
        async with session.get(abstract_url) as response:
            abstract_xml: str = await response.text()
            abstract_soup = BeautifulSoup(abstract_xml, "lxml-xml")
            abstract = abstract_soup.find("AbstractText")
            abstract_text: str = abstract.text if abstract else "Abstract not available"

        name: str = result["title"]
        authors: List[Dict[str, str]] = result["authors"]
        doi: str = result.get("elocationid", "")
        work = Work(
            id=pubmed_id,
            name=name,
            authors=authors,
            abstract=abstract_text,
            source_type=SOURCE_TYPES.OPENALEX,  # TODO
            doi=doi,
        )
        return work


async def pubmed_to_pdf_url(url: str, session: aiohttp.ClientSession) -> str:
    """
    Attempt to find a PDF URL for a given PubMed article.

    This function tries to locate a PDF link for a PubMed article by first checking
    for a PMC ID, and if not found, searching for full-text links on the PubMed page.

    Parameters
    ----------
    url : str
        The PubMed URL of the article.
    session : aiohttp.ClientSession
        An active aiohttp ClientSession for making requests.

    Returns
    -------
    str
        The URL of the PDF if found.

    Raises
    ------
    Exception
        If no full-text link is found or if there's an error fetching the page.

    Notes
    -----
    This function prioritizes PMC (PubMed Central) PDFs if available, otherwise
    it looks for any available full-text links.
    """
    print("url", url)
    pubmed_id: str = url.split("/")[-1]

    async with session.get(url) as r:
        if r.status != 200:
            raise Exception(
                f"Error fetching page for PubMed ID {pubmed_id}. Status: {r.status}"
            )
        html_text: str = await r.text()
        soup = BeautifulSoup(html_text, "html.parser")

        # First, try to find a PMC ID
        pmc_id_match = re.search(r"PMC\d+", html_text)
        if pmc_id_match:
            pmc_id: str = pmc_id_match.group(0)[3:]
            pdf_url: str = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/pdf/"
            async with session.get(pdf_url) as pdf_r:
                if pdf_r.status == 200:
                    return pdf_url

        # If no PMC ID or PDF not available, look for full-text links
        full_text_links: List[BeautifulSoup] = soup.select(".full-text-links-list a")
        for link in full_text_links:
            href: Optional[str] = link.get("href")
            if href:
                # Prioritize PDF links
                if href.endswith(".pdf") or "pdf" in href.lower():
                    return href
                else:
                    # Return the first available link if no PDF link is found
                    return href

        # If no full-text links are found
        raise Exception(f"No full-text link found for PubMed ID {pubmed_id}.")


async def likely_pdf(response: aiohttp.ClientResponse) -> bool:
    """
    Determine if a given response is likely to be a PDF.

    This function uses various heuristics to determine if the content of an
    HTTP response is likely to be a PDF file.

    Parameters
    ----------
    response : aiohttp.ClientResponse
        The HTTP response to check.

    Returns
    -------
    bool
        True if the response is likely to be a PDF, False otherwise.

    Notes
    -----
    This function checks for common text patterns in the response that might
    indicate it's not a PDF, and also checks the Content-Type header.
    """
    try:
        text: str = await response.text()
        text = text.lower()
        # Check for common patterns that indicate it's not a PDF
        if any(
            phrase in text
            for phrase in [
                "invalid article id",
                "no paper",
                "not found",
                "404",
                "error",
                "403",
                "forbidden",
            ]
        ):
            return False
    except UnicodeDecodeError:
        # If we can't decode the text, it's likely a binary file (possibly a PDF)
        return True

    # Check the Content-Type header
    if response.headers.get("Content-Type") == "application/pdf":
        return True

    return False
