from typing import Any, List, Tuple

import logging
import os
import sys
from importlib import reload
from pathlib import Path

import dotenv
import requests

dotenv.load_dotenv()

# GOOGLE_SEARCH_API_KEY = str(os.environ["INTERNET_ML_GOOGLE_API"])
# GOOGLE_SEARCH_ENGINE_ID = str(os.environ["INTERNET_ML_GOOGLE_SEARCH_ENGINE_ID"])

HTTP_USERAGENT: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
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
import itertools
import re

import aiohttp
import config
from bs4 import BeautifulSoup
from normalize import normalizer

# from relevancy import filter_irrelevant
from sentencize import sentencizer
from urlextract import URLExtract


class Google:
    def __init__(
        self: "Google",
        query: str,
        GOOGLE_SEARCH_API_KEY: str,
        GOOGLE_SEARCH_ENGINE_ID: str,
    ) -> None:
        self.__GOOGLE_SEARCH_API_KEY: str = GOOGLE_SEARCH_API_KEY
        self.__GOOGLE_SEARCH_ENGINE_ID: str = GOOGLE_SEARCH_ENGINE_ID
        self.__num_res: int = (
            5
            if config.NLP_CONF_MODE == "speed"
            else (20 if config.NLP_CONF_MODE else 10)
        )
        self.__query = query
        self.__URL_EXTRACTOR: URLExtract = URLExtract()
        self.__urls: list[str] = self.__URL_EXTRACTOR.find_urls(query)
        self.__query = re.sub(
            r"\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*", "", self.__query
        )

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
        if config.CONF_DEBUG:
            logging.info(f"Links: {self.__urls}")

    async def __fetch_url(self: "Google", session: Any, url: str) -> list[str]:
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
                logging.info(
                    f"ClientConnector Error: Likely a connection issue with wifi"
                )
            return [""]
        except Exception:
            return [""]

    async def __fetch_urls(self: "Google", urls: list[str]) -> Any:
        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.create_task(self.__fetch_url(session, url)) for url in urls
            ]
            results = await asyncio.gather(*tasks)
            return results

    def __flatten(self: Any, a: list[list[Any]]) -> list[Any]:
        return list(itertools.chain(*a))

    def __get_urls_contents(self: "Google") -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        contents = loop.run_until_complete(self.__fetch_urls(self.__urls))
        loop.close()
        self.__content = self.__flatten(contents)

    def google(self: "Google") -> tuple[list[str], list[str]]:
        # Hard coded exceptions - START
        if "Thamognya" in self.__query or "thamognya" in self.__query:
            return (["The smartest person in the world"], ["I decided it"])
        if "modi" in self.__query or "Modi" in self.__query:
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
        # Hard coded exceptions - End
        self.__get_urls()
        self.__get_urls_contents()
        return (self.__content, self.__urls)


# def google(query: str) -> tuple[list[str], list[str]]:
# return Google(query).google()


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
