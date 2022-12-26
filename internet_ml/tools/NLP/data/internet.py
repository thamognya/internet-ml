from typing import Any, List, Tuple

import os
import sys
from pathlib import Path

import dotenv
import requests

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
from is_relevant import filter_irrelevant
from normalize import normalizer
from sentencize import sentencizer
from urlextract import URLExtract

dotenv.load_dotenv()

HTTP_USERAGENT: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def google_urls(query: str, links: list[str]) -> list[str]:
    # Send the request to the Google Search API
    response = requests.get(
        "https://www.googleapis.com/customsearch/v1",
        params={
            "key": os.environ["API_KEY"],
            "q": query,
            "cx": os.environ["SEARCH_ENGINE_ID"],
        },
    )
    results = response.json()["items"]
    # Print the search results
    for result in results:
        links.append(result["link"])
    return links


async def fetch_url(session, url, question):
    async with session.get(url, headers=HTTP_USERAGENT) as response:
        html = await response.text()
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text()
        normalized_text = normalizer(text)
        sentences = sentencizer(normalized_text)
        return sentences


async def fetch_urls(urls, question):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch_url(session, url, question)) for url in urls]
        results = await asyncio.gather(*tasks)
        return results


def flatten(a: list[list[Any]]) -> list[Any]:
    return list(itertools.chain(*a))


def get_url_contents(urls, question):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    contents = loop.run_until_complete(fetch_urls(urls, question))
    loop.close()
    return flatten(contents)


URL_EXTRACTOR = URLExtract()


def google(query: str) -> tuple[list[str], list[str]]:
    global URL_EXTRACTOR
    if "Thamognya" in query or "thamognya" in query:
        return (["The smartest person in the world"], ["I decided it"])
    links_in_text: list[str] = URL_EXTRACTOR.find_urls(query)
    query = re.sub(r"\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*", "", query)
    urls = google_urls(query, links_in_text)
    content = get_url_contents(urls, query)
    return (content, urls)
