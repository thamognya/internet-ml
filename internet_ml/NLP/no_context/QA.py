# type: ignore

"""
model naming convention
# Open-AI models:
include prefix openai-*
# HuggingFace
include prefix hf-*
"""

from typing import Any, List, Tuple

import os
import sys
from pathlib import Path

import dotenv
import openai
from transformers import pipeline

sys.path.append(str(Path(__file__).parent.parent.parent) + "/tools/NLP/data")
sys.path.append(str(Path(__file__).parent.parent.parent) + "/tools/NLP")
sys.path.append(str(Path(__file__).parent.parent.parent) + "/tools")
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
    CHATGPT_CONVERSATION_ID: str = "",
    CHATGPT_PARENT_ID: str = "",
) -> tuple[Any, list[str]]:
    if OPENAI_API_KEY == "":
        OPENAI_API_KEY = str(os.environ.get("OPENAI_API_KEY"))
        openai.api_key = OPENAI_API_KEY
    if CHATGPT_SESSION_TOKEN == "":
        CHATGPT_SESSION_TOKEN = str(os.environ.get("CHATGPT_SESSION_TOKEN"))
    if CHATGPT_CONVERSATION_ID == "":
        CHATGPT_CONVERSATION_ID = str(os.environ.get("CHATGPT_CONVERSATION_ID"))
    if CHATGPT_PARENT_ID == "":
        CHATGPT_PARENT_ID = str(os.environ.get("CHATGPT_PARENT_ID"))

    if not (model.startswith("openai-") or model.startswith("hf-")):
        model = "openai-chatgpt"  # Default

    results: tuple[list[str], list[str]] = internet.Google(
        query, GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_ENGINE_ID
    ).google()

    if model.startswith("openai-"):
        if model == "openai-chatgpt":
            # ChatGPT
            prompt = f"Using the context: {' '.join(filter(lambda x: isinstance(x, str), results[0]))[:3000]} and answer the question with the context above and previous knowledge: \"{query}\". Also write long answers or essays if asked."
            print(prompt)
            exit(1)
            chatbot = Chatbot(
                {"session_token": CHATGPT_SESSION_TOKEN},
                conversation_id=None,
                parent_id=None,
            )
            response = chatbot.ask(
                prompt=prompt,
                conversation_id=None,
                parent_id=None,
            )
            return (response["message"], results[1])
        else:
            if model == "openai-text-davinci-003":
                # text-davinci-003
                prompt = f"Using the context: {' '.join(filter(lambda x: isinstance(x, str), results[0]))[:3000]} and answer the question with the context above and previous knowledge: \"{query}\". Also write long answers or essays if asked."
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    max_tokens=len(context),
                    n=1,
                    stop=None,
                    temperature=0.5,
                )
                return (response.choices[0].text, results[1])
            # TODO: add suport later
    else:
        model = model.replace("hf-", "", 1)
        qa_model = pipeline("question-answering", model=model)
        response = qa_model(question=query, context=" ".join(results[0]))
        return (response["answer"], results[1])


print(
    answer(
        query="Best original song in 80th Golden Globe award 2023?",
        model="openai-chatgpt",
    )
)
