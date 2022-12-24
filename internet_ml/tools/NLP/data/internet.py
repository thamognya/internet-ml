#type: ignore
from typing import Any, Dict, List, Tuple

import asyncio
import logging
import re
import time
import urllib

import aiohttp
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(
    filename="internet.log",
    filemode="w",
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s",
)

# import concurrent.futures

# Import the config module
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.parent) + "/utils/NLP")
sys.path.append(str(Path(__file__).parent.parent.parent.parent) + "/utils")
import config

sys.path.append(str(Path(__file__).parent.parent))
import pickle

from is_relevant import filter_irrelevant
from normalize import normalizer
from sentencize import sentencizer
from urlextract import URLExtract

# Define the user agent
HTTP_USERAGENT: dict[str, str] = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
# Define the google domains
UNWANTED_DOMAINS = {
    "https://www.google.",
    "https://google.",
    "https://webcache.googleusercontent.",
    "http://webcache.googleusercontent.",
    "https://policies.google.",
    "https://support.google.",
    "https://maps.google.",
    "https://youtube.",
    "https://translate.google.",
}

CACHE_FILE_PATH: str = "./internet_cache.pkl"
CACHE_TIME: int = 86400  # one day

URL_EXTRACTOR = URLExtract()

# Load the cache from the file (if it exists)
try:
    with open(CACHE_FILE_PATH, "rb") as f:
        cache: Any = pickle.load(f)
except FileNotFoundError:
    cache: Any = {}


# Define the fetch_url function
async def fetch_url(session: aiohttp.ClientSession, url: str) -> str:
    global HTTP_USERAGENT
    async with session.get(url, headers=HTTP_USERAGENT) as response:
        return await response.text()


# Define the google_urls function
async def google_urls(query: str, links: list[str]) -> list[str]:
    """
    Asynchronously search Google for the given query and retrieve the URLs of the top results.

    Parameters:
        query (str): The query to search for.

    Returns:
        List[str]: A list of the URLs of the top search results.
    """
    global UNWANTED_DOMAINS
    # Initialize an empty list to store the URLs
    urls: list[str] = links

    # Determine the number of results to retrieve based on the configuration mode
    num_of_res: int = (
        5
        if config.NLP_CONF_MODE == "speed"
        else (20 if config.NLP_CONF_MODE == "accuracy" else 10)
    )

    # Log the number of results wanted (if debugging is enabled)
    if config.NLP_CONF_DEBUG:
        logging.info(f"number of results wanted: {num_of_res}")

    # Construct the search URL
    search_url: str = (
        "https://www.google.com/search?q="
        + str(urllib.parse.quote_plus(query))
        + "&num="
        + str(num_of_res)
    )

    # Log the search URL (if debugging is enabled)
    if config.NLP_CONF_DEBUG:
        logging.info(f"url: {search_url}")

    # Create an aiohttp session and use it to fetch the search results
    async with aiohttp.ClientSession() as session:
        response: str = await fetch_url(session, search_url)

        # Wait 10 seconds before parsing the results (to avoid being rate-limited)
        await asyncio.sleep(10.0)

        # Parse the search results using BeautifulSoup
        soup: BeautifulSoup = BeautifulSoup(response, "html.parser")

        # Iterate over the links in the search results
        for link in list(soup.select("a[href]")):
            # Extract the URL from the link
            url = str(link["href"])

            # Check if the URL is valid and not a Google or YouTube link
            if ("http" in url) and (
                not any(url.startswith(s) for s in UNWANTED_DOMAINS)
            ):
                urls.append(url)
                if config.NLP_CONF_DEBUG:
                    logging.info(f"added {url}")
            if len(urls) == num_of_res:
                break
    return urls


async def fetch_url_text(
    session: aiohttp.ClientSession, url: str, query: str
) -> list[str]:
    """
    Extract the text from the given HTML content.

    Parameters:
        session (aiohttp.ClientSession): aiohttp session
        url (str): The url content to get text from.

    Returns:
        str: The extracted text.
    """
    global HTTP_USERAGENT
    try:
        async with session.get(url, headers=HTTP_USERAGENT) as response:
            soup: BeautifulSoup = BeautifulSoup(await response.text(), "html.parser")
            text = normalizer(soup.get_text())
            if config.NLP_CONF_DEBUG:
                logging.info(f"Text: {text}")
            sentences: list[str] = sentencizer(text)
            sentences = filter_irrelevant(sentences, query)
            return sentences
    except Exception as e:
        # Log the error and continue execution
        logging.error(f"Error occurred: {e}")
        return []


def flatten(l):
    return [item for sublist in l for item in sublist]


async def get_text_content(urls: list[str], query: str) -> list[str]:
    # Create a list to store the results
    results: list[str] = []
    # Create an aiohttp session
    async with aiohttp.ClientSession() as session:
        # Create a list of tasks to run concurrently
        tasks: list[Any] = [
            asyncio.create_task(fetch_url_text(session, url, query)) for url in urls
        ]
        # Use asyncio.gather to run the tasks concurrently
        results = await asyncio.gather(*tasks)
    sentences: list[str] = flatten(results)
    return sentences


def google(query: str) -> Tuple[List[str], str]:
    global cache, CACHE_FILE_PATH, CACHE_TIME, URL_EXTRACTOR
    links_in_text: list[str] = URL_EXTRACTOR.find_urls(query)
    query = re.sub(r"\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*", "", query)
    entry = cache.get(query)
    if entry is None:
        # no query exists, so add a new entry to the cache
        urls: List[str] = asyncio.run(google_urls(query, links_in_text))
        text: str = str(asyncio.run(get_text_content(urls, query)))
        cache[query]: Tuple[Tuple[List[str], str], int] = (
            (text, urls),
            time.time() + CACHE_TIME,
        )  # cache expires in one hour
    elif entry[1] < time.time():
        # update as it expired
        urls: List[str] = asyncio.run(google_urls(query, links_in_text))
        text: str = str(asyncio.run(get_text_content(urls, query)))
        cache[query]: Tuple[Tuple[List[str], str], int] = (
            (text, urls),
            time.time() + CACHE_TIME,
        )  # cache expires in one hour
    else:
        # available so return it
        text: List[str] = entry[0][0]
        urls: str = entry[0][1]
    # Save the cache to the file
    with open(CACHE_FILE_PATH, "wb") as f:
        pickle.dump(cache, f)
    # Return the text
    return (text, urls)


"""
async + multithreading since web scraping is I/O bound
https://stackoverflow.com/questions/27435284/multiprocessing-vs-multithreading-vs-asyncio
normal
________________________________________________________
Executed in    1.67 secs      fish           external
   usr time  137.29 millis    0.11 millis  137.18 millis
   sys time   38.39 millis    1.25 millis   37.13 millis
Async
________________________________________________________
Executed in  624.82 millis    fish           external
   usr time  141.92 millis    0.11 millis  141.81 millis
   sys time   38.00 millis    1.45 millis   36.55 millis

concurrent
________________________________________________________
Executed in  629.67 millis    fish           external
   usr time  136.72 millis    0.12 millis  136.60 millis
   sys time   36.86 millis    1.32 millis   35.54 millis

multiprocessing
________________________________________________________
Executed in  754.61 millis    fish           external
   usr time  399.25 millis    0.11 millis  399.14 millis
   sys time  164.39 millis    1.49 millis  162.90 millis

multiprocessing

OVERALL
multithreading bs4
________________________________________________________
Executed in   14.67 secs    fish           external
   usr time    1.81 secs    0.12 millis    1.81 secs
   sys time    0.14 secs    1.50 millis    0.14 secs
multiprocessing bs4
"""
