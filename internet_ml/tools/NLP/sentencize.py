from typing import Any, List

import logging

# logging config
logging.basicConfig(
    filename="sentencize.log",
    filemode="w",
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s",
)

import sys
from pathlib import Path

# Add utils directory to path
sys.path.append(str(Path(__file__).parent.parent.parent) + "/utils/NLP")
sys.path.append(str(Path(__file__).parent.parent.parent) + "/utils")
import concurrent.futures

import config
import nltk

nltk.download("words", quiet=True)

ENGLISH_WORDS: Any = set(nltk.corpus.words.words())


def convert_to_english(text: str) -> str:
    global ENGLISH_WORDS
    return " ".join(
        w
        for w in nltk.wordpunct_tokenize(text)
        if w.lower() in ENGLISH_WORDS or not w.isalpha()
    )


def sentencizer(text: str) -> list[str]:
    global convert_to_english
    inital_sentences: list[str] = nltk.tokenize.sent_tokenize(text)
    english_sentences: list[str] = []

    # Use concurrent.futures.ThreadPoolExecutor to process the sentences concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
        # Create a list of futures to process the sentences concurrently
        futures = [
            executor.submit(convert_to_english, sentence)
            for sentence in inital_sentences
        ]
        # Use concurrent.futures.as_completed to retrieve the results of the futures as they complete
        for future in concurrent.futures.as_completed(futures):
            english_sentences.append(future.result())

    if config.CONF_DEBUG:
        logging.info(f"sentences: {english_sentences}")
    return english_sentences


# print(sentencizer("hello gdfjsfkjd. i amf dfjdslf the greatest efe ve every"))
