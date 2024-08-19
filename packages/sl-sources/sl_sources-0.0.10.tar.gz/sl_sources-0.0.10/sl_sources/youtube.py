import asyncio
import glob
import json
import os
import re
import tempfile
import urllib.parse
from multiprocessing import Pool
from typing import List, Optional, Dict, Any
from uuid import uuid4

import requests
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL

from .models import ENTITY_TYPES, SOURCE_TYPES, WORK_TYPES, Author, SearchInput, Work
from .audio_transcriber import transcribe

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_youtube_data(url: str) -> str:
    """
    Fetch HTML data from a YouTube URL.

    Parameters
    ----------
    url : str
        The YouTube URL to fetch data from.

    Returns
    -------
    str
        The HTML content of the YouTube page.

    Raises
    ------
    requests.RequestException
        If there's an error fetching data from YouTube.
    """
    try:
        response = requests.get(url=url)
        response.raise_for_status()
    except requests.RequestException:
        raise requests.RequestException("Failed to fetch data from YouTube.")
    return response.text


def search_by_url(url: str) -> Work:
    """
    Search for a YouTube video by its URL and create a Work object.

    Parameters
    ----------
    url : str
        The URL of the YouTube video.

    Returns
    -------
    Work
        A Work object containing information about the video.

    Raises
    ------
    ValueError
        If the provided URL is not valid.
    """
    if "https://" in url:
        response = fetch_youtube_data(url)
        soup_obj = BeautifulSoup(response, features="lxml")
        video_id = re.search(r"(?<=\?v=)[\w-]+", url).group(0)
        title = soup_obj.find("meta", {"name": "title"})["content"]
        js_script = str(soup_obj.find_all("script")[-12])
        duration_mil = re.search(r'"approxDurationMs":"(\d+)"', js_script).group(1)
        description = soup_obj.find("meta", {"name": "description"})["content"]
        if description is None:
            description_element = soup_obj.select_one("#eow-description")
            if description_element:
                description = description_element.get_text(strip=True)
            else:
                description = ""

        return Work(
            id=video_id,
            name=title,
            work_type=WORK_TYPES.VIDEO,
            url=url,
            duration=duration_mil,
            abstract=description,
            source_type=SOURCE_TYPES.YOUTUBE,
        )
    else:
        raise ValueError("Please provide valid URL.")


def search_by_term(term: str, max_results: Optional[int] = None) -> List[Work]:
    """
    Search YouTube for videos based on a search term.

    Parameters
    ----------
    term : str
        The search term to use.
    max_results : Optional[int], optional
        The maximum number of results to return. If None, returns all results.

    Returns
    -------
    List[Work]
        A list of Work objects representing the search results.
    """
    encoded_search = urllib.parse.quote_plus(term)
    BASE_URL = "https://youtube.com"
    url = f"{BASE_URL}/results?search_query={encoded_search}&sp=CAM"
    response = fetch_youtube_data(url)

    results = []
    searched_obj = _prepare_data(response)

    for contents in searched_obj:
        for video in contents["itemSectionRenderer"]["contents"]:
            if "videoRenderer" in video.keys():
                video_data = video.get("videoRenderer", {})

                # Extract the year from the publishedTimeText
                published_time_text = video_data.get("publishedTimeText", {}).get(
                    "simpleText", ""
                )
                year_match = re.search(r"\b(\d{4})\b", published_time_text)
                year = int(year_match.group(1)) if year_match else None

                abstract = (
                    video_data.get("descriptionSnippet", {})
                    .get("runs", [{}])[0]
                    .get("text", "")
                )
                if not abstract:
                    abstract = (
                        video_data.get("detailedMetadataSnippets", [{}])[0]
                        .get("snippetText", {})
                        .get("runs", [{}])[0]
                        .get("text", "")
                    )

                work = Work(
                    id=video_data.get("videoId", str(uuid4())),
                    name=video_data.get("title", {}).get("runs", [[{}]])[0].get("text"),
                    work_type=WORK_TYPES.VIDEO,
                    abstract=abstract,
                    url=f"{BASE_URL}{video_data.get('navigationEndpoint', {}).get('commandMetadata', {}).get('webCommandMetadata', {}).get('url')}",
                    duration=video_data.get("lengthText", {}).get("simpleText", "0"),
                    authors=[
                        Author(
                            name=video_data.get("longBylineText", {})
                            .get("runs", [[{}]])[0]
                            .get("text"),
                            source_type=SOURCE_TYPES.YOUTUBE,
                        )
                    ],
                    year=year,
                    source_type=SOURCE_TYPES.YOUTUBE,
                )
                results.append(work)

        if results:
            if max_results is not None and len(results) > max_results:
                return results[:max_results]

        break

    return results


def _prepare_data(response: str) -> List[Dict[str, Any]]:
    """
    Extract and prepare the search data from the YouTube response.

    Parameters
    ----------
    response : str
        The HTML response from YouTube.

    Returns
    -------
    List[Dict[str, Any]]
        A list of dictionaries containing the search results data.
    """
    start = response.index("ytInitialData") + len("ytInitialData") + 3
    end = response.index("};", start) + 1
    json_str = response[start:end]
    data = json.loads(json_str)
    searched_obj = data["contents"]["twoColumnSearchResultsRenderer"][
        "primaryContents"
    ]["sectionListRenderer"]["contents"]

    return searched_obj


async def search_youtube(search_input: SearchInput) -> List[Work]:
    """
    Asynchronous function to search YouTube based on the provided search input.

    Parameters
    ----------
    search_input : SearchInput
        The search input containing the query and number of results.

    Returns
    -------
    List[Work]
        A list of Work objects representing the search results.
    """
    query = search_input.query
    num_results = search_input.num_results
    search_results = search_by_term(query, max_results=num_results)
    results = []

    for search_result in search_results:
        results.append(search_result)

    return results


def download_video(url: str, temp_dir: str) -> str:
    """
    Download a YouTube video's audio.

    Parameters
    ----------
    url : str
        The URL of the YouTube video.
    temp_dir : str
        The temporary directory to save the downloaded audio.

    Returns
    -------
    str
        The path to the downloaded audio file.
    """
    ydl_opts = {
        "overwrites": True,
        "format": "bestaudio",
        "outtmpl": os.path.join(temp_dir, "audio.mp3"),
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)
        return os.path.join(temp_dir, "audio.mp3")


def format_timestamp(
    seconds: float, always_include_hours: bool = False, decimal_marker: str = "."
) -> str:
    """
    Format a timestamp from seconds to a string representation.

    Parameters
    ----------
    seconds : float
        The number of seconds to format.
    always_include_hours : bool, optional
        Whether to always include hours in the output, by default False.
    decimal_marker : str, optional
        The character to use as the decimal marker, by default ".".

    Returns
    -------
    str
        The formatted timestamp string.
    """
    if seconds is not None:
        milliseconds = round(seconds * 1000.0)
        hours = milliseconds // 3_600_000
        milliseconds -= hours * 3_600_000
        minutes = milliseconds // 60_000
        milliseconds -= minutes * 60_000
        seconds = milliseconds // 1_000
        milliseconds -= seconds * 1_000
        hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
        return f"{hours_marker}{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"
    else:
        return str(seconds)


def download_from_youtube_sync(work: Work) -> Work:
    """
    Synchronous function to download and process a YouTube video.

    This function attempts to download subtitles if available, otherwise
    it downloads the audio and transcribes it.

    Parameters
    ----------
    work : Work
        The Work object representing the YouTube video.

    Returns
    -------
    Work
        The updated Work object with the full text (transcript) added.
    """
    print(f"Downloading video from youtube: {work.url}")
    print(work)

    with tempfile.TemporaryDirectory() as temp_dir:
        ydl_opts = {
            "writesubtitles": True,
            "subtitleslangs": ["en"],
            "subtitlesformat": "vtt",
            "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
            "skip_download": True,
            "quiet": False,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([work.url])

        vtt_files = glob.glob(os.path.join(temp_dir, "*.vtt"))
        if vtt_files:
            vtt_file = vtt_files[0]
            try:
                with open(vtt_file, "r", encoding="utf-8") as f:
                    vtt_data = f.read()
                transcript = vtt_to_text(vtt_data)
                work.full_text = transcript
                return work
            except Exception as e:
                print(f"Error reading VTT file: {e}")
        else:
            print("No VTT file found, attempting to transcribe audio with Whisper")
            try:
                id = work.url.split("v=")[1].split("&")[0]
                audio_file = os.path.join(temp_dir, f"{id}")

                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": audio_file,
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ],
                }

                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([work.url])

                if os.path.exists(audio_file + ".mp3"):
                    work.full_text = transcribe(audio_file + ".mp3")
                    return work
                else:
                    print(f"Error: Audio file {audio_file}.mp3 not found.")
                    return work
            except Exception as e:
                print(f"Error in audio transcription: {e}")
                return work


async def download_from_youtube(work: Work) -> Work:
    """
    Asynchronous wrapper for the synchronous download_from_youtube_sync function.

    Parameters
    ----------
    work : Work
        The Work object representing the YouTube video.

    Returns
    -------
    Work
        The updated Work object with the full text (transcript) added.
    """
    loop = asyncio.get_running_loop()
    with Pool(processes=1) as pool:
        result = await loop.run_in_executor(
            None, pool.apply, download_from_youtube_sync, (work,)
        )
    return result


def vtt_to_text(vtt_data: str) -> str:
    """
    Convert VTT subtitle data to plain text.

    Parameters
    ----------
    vtt_data : str
        The VTT subtitle data as a string.

    Returns
    -------
    str
        The extracted text from the VTT data.
    """
    print("Converting VTT to text")
    lines = vtt_data.strip().split("\n")
    transcript = []

    for line in lines[2:]:
        if "-->" not in line and not line.strip().isdigit():
            transcript.append(line.strip())

    return " ".join(transcript)


async def search_and_download_from_youtube(search_input: SearchInput) -> List[Work]:
    """
    Search YouTube and download the results.

    This function searches YouTube based on the provided search input,
    then downloads and processes each result.

    Parameters
    ----------
    search_input : SearchInput
        The search input containing the query and number of results.

    Returns
    -------
    List[Work]
        A list of Work objects with full text (transcripts) added.
    """
    try:
        logger.info(f"Searching YouTube for: {search_input.query}")
        search_results = await search_youtube(search_input)
        logger.info(f"Found {len(search_results)} search results")

        if not search_results:
            logger.warning("No search results found")
            return []

        works = []

        for work in search_results:
            try:
                logger.info(f"Downloading and processing video: {work.url}")
                downloaded_work = await download_from_youtube(work)
                if downloaded_work and downloaded_work.full_text:
                    works.append(downloaded_work)
                else:
                    logger.warning(f"Failed to process video: {work.url}")
            except Exception as e:
                logger.error(f"Error processing video {work.url}: {str(e)}")

        logger.info(f"Successfully processed {len(works)} videos")
        return works
    except Exception as e:
        logger.error(f"Error in search_and_download_from_youtube: {str(e)}")
        return []
