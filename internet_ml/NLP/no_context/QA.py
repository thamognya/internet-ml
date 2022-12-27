from typing import Any, List, Tuple

import logging
import sys
from pathlib import Path

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

QA_MODEL: Any = pipeline("question-answering")


def answer(
    query: str,
    GOOGLE_API_KEY: str = config.GOOGLE_API_KEY,
    GOOGLE_SEARCH_ENGINE_ID: str = config.GOOGLE_SEARCH_ENGINE_ID,
) -> tuple[Any, list[str]]:
    global QA_MODEL
    results: tuple[list[str], list[str]] = internet.google(
        query, GOOGLE_API_KEY, GOOGLE_SEARCH_ENGINE_ID
    )
    answer: tuple[Any, list[str]] = (
        QA_MODEL(question=query, context=str(results[0])),
        results[1],
    )
    if config.CONF_DEBUG:
        logging.info(f"Answer: {answer}")
    return answer


# def custom_answer
