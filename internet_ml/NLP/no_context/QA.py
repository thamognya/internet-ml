from typing import Any, List, Tuple

import logging
import os
import sys
from pathlib import Path

import dotenv
import openai
from transformers import list_models, pipeline

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

dotenv.load_dotenv()


def answer(
    query: str,
    model: str = "openai-ChatGPT",
    GOOGLE_SEARCH_API_KEY: str = "",
    GOOGLE_SEARCH_ENGINE_ID: str = "",
    OPENAI_API_KEY: str = "",
    CHATGPT_SESSION_TOKEN: str = "",
) -> tuple[Any, list[str]]:
    # if environment keys are not given, assume it is in env
    if GOOGLE_SEARCH_API_KEY == "":
        GOOGLE_SEARCH_API_KEY = str(os.environ.get("GOOGLE_SEARCH_API_KEY"))
    if GOOGLE_SEARCH_ENGINE_ID == "":
        GOOGLE_SEARCH_ENGINE_ID = str(os.environ.get("GOOGLE_SEARCH_ENGINE_ID"))
    if OPENAI_API_KEY == "":
        OPENAI_API_KEY = str(os.environ.get("OPENAI_API_KEY"))
        openai.api_key = OPENAI_API_KEY
    if CHATGPT_SESSION_TOKEN == "":
        CHATGPT_SESSION_TOKEN = str(os.environ.get("CHATGPT_SESSION_TOKEN"))
    """
    model naming convention
    # Open-AI models:
    include prefix openai-*
    # HuggingFace
    include prefix hf-*
    # 
    """
    if not (model.startswith("openai-") == 0 or model.startswith("hf-") == 0):
        model = "openai-ChatGPT"  # Default

    answer: str = ""
    if model.startswith("openai-") == 0:
        # results: tuple[list[str], list[str]] = internet.Google(
        #     query, GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_ENGINE_ID
        # ).google(filter_irrelevant=True)
        print("hi")
    else:
        models = [
            model
            for model in list_models()
            if "qa" in model or "question-answering" in model
        ]
        model = model.replace("hf-", "", 1)
        if not model in models:
            model = "hf-"
        # results: tuple[list[str], list[str]] = internet.Google(
        #     query, GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_ENGINE_ID
        # ).google(filter_irrelevant=False)

    answer_result: tuple[Any, list[str]] = (answer, ["hi"])  # results[1])
    if config.CONF_DEBUG:
        logging.info(f"Answer: {answer_result}")
    return answer_result


# print(os.environ)
print(answer("What is the newest Pokemon Game?"))
# def custom_answer
