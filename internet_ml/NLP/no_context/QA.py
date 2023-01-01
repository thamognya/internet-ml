from typing import Any, List, Tuple

import logging
import os
import sys
from pathlib import Path

import dotenv
from transformers import pipeline

logging.basicConfig(
    filename="QA.log",
    filemode="w",
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s",
)

sys.path.append(str(Path(__file__).parent.parent.parent) + "/tools/NLP/data")
sys.path.append(str(Path(__file__).parent.parent.parent) + "/utils")
import config
import internet


def answer(
    query: str, GOOGLE_SEARCH_API_KEY: str, GOOGLE_SEARCH_ENGINE_ID: str
) -> tuple[Any, list[str]]:
    QA_MODEL: Any = pipeline("question-answering")
    results: tuple[list[str], list[str]] = internet.Google(
        query, GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_ENGINE_ID
    ).google()
    answer: tuple[Any, list[str]] = (
        QA_MODEL(question=query, context=str(results[0])),
        results[1],
    )
    if config.CONF_DEBUG:
        logging.info(f"Answer: {answer}")
    return answer


# print(os.environ)
# print(answer("Who is Elon Musk?"))
# def custom_answer
