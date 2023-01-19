from typing import Any, List, Tuple

import asyncio
import concurrent.futures
import itertools
import os
import re
import sys
from importlib import reload
from pathlib import Path

import aiohttp
import dotenv
import requests
from bs4 import BeautifulSoup

HTTP_USERAGENT: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

sys.path.append(str(Path(__file__).parent.parent.parent.parent) + "/utils/NLP")
sys.path.append(str(Path(__file__).parent.parent.parent.parent) + "/utils")
sys.path.append(str(Path(__file__).parent.parent))

import config
from adremover import AdRemover
from keywords import get_keywords
from normalize import normalizer
from relevancy import filter_relevant
from sentencize import sentencizer
from urlextract import URLExtract

dotenv.load_dotenv()


class Google:
    def __init__(
        self: "Google",
        query: str,
        GOOGLE_SEARCH_API_KEY: str,
        GOOGLE_SEARCH_ENGINE_ID: str,
    ) -> None:
        # if environment keys are not given, assume it is in env
        if GOOGLE_SEARCH_API_KEY == "":
            self.__GOOGLE_SEARCH_API_KEY = str(os.environ.get("GOOGLE_SEARCH_API_KEY"))
        if GOOGLE_SEARCH_ENGINE_ID == "":
            self.__GOOGLE_SEARCH_ENGINE_ID = str(
                os.environ.get("GOOGLE_SEARCH_ENGINE_ID")
            )
        self.__num_res: int = (
            5
            if config.NLP_CONF_MODE == "speed"
            else (20 if config.NLP_CONF_MODE else 10)
        )
        self.__query = query
        self.__URL_EXTRACTOR: URLExtract = URLExtract()
        self.__urls: list[str] = self.__URL_EXTRACTOR.find_urls(query)
        self.__query = str(
            re.sub(
                r"\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*",
                "",
                str(self.__query),
            )
        )
        self.__content: list[str] = []
        ADBLOCK_RULES = [
            "https://easyList-downloads.adblockplus.org/ruadList+easyList.txt",
            "https://filters.adtidy.org/extension/chromium/filters/1.txt",
        ]
        self.__ad_remover = AdRemover(ADBLOCK_RULES)

    def __get_urls(self: "Google") -> None:
        # Send the request to the Google Search API
        if self.__GOOGLE_SEARCH_API_KEY == "":
            exit("ERROR: Google API Key not found")
        if self.__GOOGLE_SEARCH_ENGINE_ID == "":
            exit("ERROR: Google Search Engine Id not found")
        response = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={
                "key": self.__GOOGLE_SEARCH_API_KEY,
                "q": self.__query,
                "cx": self.__GOOGLE_SEARCH_ENGINE_ID,
            },
        )
        results = response.json()["items"]
        for result in results:
            self.__urls.append(result["link"])
            if len(self.__urls) == self.__num_res:
                break

    def __flatten(self: Any, a: list[list[Any]]) -> list[Any]:
        return list(itertools.chain(*a))

    async def __fetch_url(self: "Google", session: Any, url: str) -> str:
        try:
            async with session.get(url, headers=HTTP_USERAGENT) as response:
                html = await response.text()
                # html = self.__ad_remover.remove_ads(html)
                soup = BeautifulSoup(html, "html.parser")
                text = soup.get_text()
                normalized_text = normalizer(text)
                return normalized_text
        except Exception:
            error: str = ""
            return error

    async def __fetch_urls(self: "Google", urls: list[str]) -> list[str]:
        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.create_task(self.__fetch_url(session, url)) for url in urls
            ]
            results: list[str] = await asyncio.gather(*tasks)
            return results

    def __get_urls_contents(self: "Google") -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        contents = loop.run_until_complete(self.__fetch_urls(self.__urls))
        loop.close()
        self.__content = contents

    def __filter_irrelevant_processing(self: "Google") -> None:
        with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
            futures = [executor.submit(filter_relevant, self.__content, self.__query)]
            concurrent.futures.wait(futures)
            content: list[str] = []
            for future in futures:
                content.append(future.result())
            self.__content = content

    def google(
        self: "Google", filter_irrelevant: bool = True
    ) -> tuple[list[str], list[str]]:
        self.__get_urls()
        self.__get_urls_contents()
        if filter_irrelevant:
            self.__filter_irrelevant_processing()
        results: tuple[list[str], list[str]] = (self.__content, self.__urls)  # type: ignore
        return results


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
