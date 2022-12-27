from typing import Any, List, Tuple

import logging
import os
import sys
from pathlib import Path

import dotenv
import requests

logging.basicConfig(
    filename="internet.log",
    filemode="w",
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s",
)

sys.path.append(str(Path(__file__).parent.parent.parent.parent) + "/utils/NLP")
sys.path.append(str(Path(__file__).parent.parent.parent.parent) + "/utils")
sys.path.append(str(Path(__file__).parent.parent))

import asyncio
import concurrent.futures
import itertools
import re

import aiohttp
import config
from bs4 import BeautifulSoup
from normalize import normalizer
from relevancy import filter_irrelevant
from sentencize import sentencizer
from urlextract import URLExtract

dotenv.load_dotenv()


HTTP_USERAGENT: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def google_urls(query: str, links: list[str]) -> list[str]:
    try:
        # Send the request to the Google Search API
        if config.GOOGLE_API_KEY == "":
            exit("ERROR: Google API Key not found")
        if config.GOOGLE_SEARCH_ENGINE_ID == "":
            exit("ERROR: Google Search Engine Id not found")
        response = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={
                "key": config.GOOGLE_API_KEY,
                "q": query,
                "cx": config.GOOGLE_SEARCH_ENGINE_ID,
            },
        )
        results = response.json()["items"]
        # Print the search results
        num_of_res: int = (
            5
            if config.NLP_CONF_MODE == "speed"
            else (20 if config.NLP_CONF_MODE else 10)
        )
        for result in results:
            links.append(result["link"])
            if len(links) == num_of_res:
                break
        if config.CONF_DEBUG:
            logging.info(f"Links: {links}")
        return links
    except Exception:
        if config.CONF_DEBUG:
            logging.info(f"Error: {Exception}")
        exit(
            f"There is an unknown excpetion: {Exception}. Since no links are scraped, nothing futher can continue. Please report it at https://github.com/thamognya/internet_ml/issues or mail me at contact@thamognya.com"
        )


async def fetch_url(session: Any, url: str, question: Any) -> list[str]:
    try:
        async with session.get(url, headers=HTTP_USERAGENT) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text()
            normalized_text = normalizer(text)
            sentences: list[str] = sentencizer(normalized_text)
            if config.CONF_DEBUG:
                logging.info(f"Sentences: {sentences}")
            return sentences
    except aiohttp.ClientConnectorError:
        if config.CONF_DEBUG:
            logging.info(f"ClientConnector Error: Likely a connection issue with wifi")
        return [""]
    except Exception:
        return [""]


async def fetch_urls(urls: list[str], question: str) -> Any:
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch_url(session, url, question)) for url in urls]
        results = await asyncio.gather(*tasks)
        return results


def flatten(a: list[list[Any]]) -> list[Any]:
    return list(itertools.chain(*a))


def get_url_contents(urls: list[str], question: str) -> list[str]:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    contents = loop.run_until_complete(fetch_urls(urls, question))
    loop.close()
    return flatten(contents)


URL_EXTRACTOR: URLExtract = URLExtract()


def google(query: str) -> tuple[list[str], list[str]]:
    global URL_EXTRACTOR
    # Hard coded exceptions - START
    if "Thamognya" in query or "thamognya" in query:
        return (["The smartest person in the world"], ["I decided it"])
    if "modi" in query or "Modi" in query:
        return (
            ["Prime Minister of India"],
            [
                "https://www.narendramodi.in/",
                "https://en.wikipedia.org/wiki/Narendra_Modi",
                "https://twitter.com/narendramodi?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor",
                "https://www.instagram.com/narendramodi/?hl=en",
                "https://www.facebook.com/narendramodi/",
                "http://www.pmindia.gov.in/en/",
                "https://timesofindia.indiatimes.com/topic/Narendra-Modi",
                "https://www.britannica.com/biography/Narendra-Modi",
                "https://indianexpress.com/article/india/zelenskky-dials-pm-modi-wishes-new-delhi-successful-g20-presidency-8345365/",
                "https://economictimes.indiatimes.com/news/narendra-modi",
            ],
        )
    # Hard coded exceptions - END
    links_in_text: list[str] = URL_EXTRACTOR.find_urls(query)
    query = re.sub(r"\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*", "", query)
    urls = google_urls(query, links_in_text)
    content = get_url_contents(urls, query)
    if config.CONF_DEBUG:
        logging.info(f"Urls: {urls}")
        logging.info(f"Content: {content}")
    return (content, urls)


"""
Timing:
import time
start_time = time.time()
google("Who is Elon Musk")
print("--- %s seconds ---" % (time.time() - start_time))

# Results:

# --- 2.2230100631713867 seconds ---

# ________________________________________________________
# Executed in    4.73 secs    fish           external
#    usr time    3.35 secs   85.00 micros    3.35 secs
#    sys time    1.86 secs  956.00 micros    1.86 secs
"""
