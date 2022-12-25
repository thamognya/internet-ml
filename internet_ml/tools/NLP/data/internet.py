# type: ignore
from typing import List

import asyncio
import functools
import multiprocessing
import os

import aiohttp
import dotenv
import requests

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


class LinkFetcher:
    def __init__(self, urls):
        self.urls = urls

    async def fetch(self, session, url):
        async with session.get(url, headers=HTTP_USERAGENT) as response:
            return await response.text()

    async def main(self, session):
        tasks = [asyncio.ensure_future(self.fetch(session, url)) for url in self.urls]
        responses = await asyncio.gather(*tasks)
        return responses


def fetch_content(urls: list[str]):
    fetcher = LinkFetcher(urls)
    with aiohttp.ClientSession() as session:
        with multiprocessing.Pool(processes=5) as pool:
            contents = list(pool.map(functools.partial(fetcher.main), [session]))
    return contents


a = google_urls("Who is Neil Armstrong", [])
print(a)
print(fetch_content(a))
