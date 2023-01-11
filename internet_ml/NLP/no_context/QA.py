# type: ignore
from typing import Any, List, Tuple

import logging
import os
import sys
from pathlib import Path

import dotenv
import openai
from transformers import pipeline

logging.basicConfig(
    filename="QA.log",
    filemode="w",
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s",
)

sys.path.append(str(Path(__file__).parent.parent.parent) + "/tools/NLP/data")
sys.path.append(str(Path(__file__).parent.parent.parent) + "/tools/NLP")
sys.path.append(str(Path(__file__).parent.parent.parent) + "/utils")
import config
import internet
from ChatGPT import Chatbot

dotenv.load_dotenv()


def answer(
    query: str,
    model: str = "openai-chatgpt",
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
    if not (model.startswith("openai-") or model.startswith("hf-")):
        model = "openai-chatgpt"  # Default

    if model.startswith("openai-"):
        if model == "openai-chatgpt":
            # ChatGPT
            results: tuple[list[str], list[str]] = internet.Google(
                query, GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_ENGINE_ID
            ).google(filter_irrelevant=False)
            print(results)
            chatbot = Chatbot(
                {"session_token": CHATGPT_SESSION_TOKEN},
                conversation_id=None,
                parent_id=None,
            )
            response = chatbot.ask(
                f"Utilize the following context: {results[0]} ontop of existing knowledge and answer the question: {query}",
                conversation_id=None,
                parent_id=None,
            )
            return (response.message, results[1])
        else:
            if model == "openai-text-davinci-003":
                results: tuple[list[str], list[str]] = internet.Google(
                    query, GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_ENGINE_ID
                ).google(filter_irrelevant=True)
                context = " ".join(results[0])
                context[: (4097 - len(query) - 10)]
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=f"{context} Q: {query}",
                    max_tokens=len(context),
                    n=1,
                    stop=None,
                    temperature=0.5,
                )
                return (response.choices[0].text, results[1])
            # TODO: add suport later
    else:
        model = model.replace("hf-", "", 1)
        results: tuple[list[str], list[str]] = internet.Google(
            query, GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_ENGINE_ID
        ).google(filter_irrelevant=False)
        qa_model = pipeline("question-answering", model=model)
        response = qa_model(question=query, context=" ".join(results[0]))
        return (response["answer"], results[1])


# print(os.environ)
# print(answer(query="What is the newest Pokemon Game?", model="hf-deepset/deberta-v3-base-squad2"))
# def custom_answer
