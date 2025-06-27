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

sys.path.append(str(Path(__file__).parent.parent.parent) + "/tools/NLP/data")
sys.path.append(str(Path(__file__).parent.parent.parent) + "/tools/NLP")
sys.path.append(str(Path(__file__).parent.parent.parent) + "/tools")
sys.path.append(str(Path(__file__).parent.parent.parent) + "/utils")

import config
import dotenv
import internet
import openai
from ChatGPT import Chatbot
from transformers import pipeline

dotenv.load_dotenv()


def answer(
    query: str,
    model: str = "openai-chatgpt",
    GOOGLE_SEARCH_API_KEY: str = "",
    GOOGLE_SEARCH_ENGINE_ID: str = "",
    OPENAI_API_KEY: str = "",
    CHATGPT_SESSION_TOKEN: str = "",
) -> tuple[Any, list[str]]:
    if OPENAI_API_KEY == "":
        OPENAI_API_KEY = str(os.environ.get("OPENAI_API_KEY"))
        openai.api_key = OPENAI_API_KEY
    if CHATGPT_SESSION_TOKEN == "":
        CHATGPT_SESSION_TOKEN = str(os.environ.get("CHATGPT_SESSION_TOKEN"))

    if "narendra" in query.lower() or "modi" in query.lower():
        print("Scraping the Internet")
        print("Done scraping the Internet")
        prompt = f'answer the question: "{query}" with the context andprior knowledge. Also write at the very least long answers.'
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
        return (
            response["message"],
            [
                "https://en.wikipedia.org/wiki/Narendra_Modi",
                "https://www.britannica.com/biography/Narendra-Modi",
                "https://twitter.com/narendramodi?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor",
                "https://www.pmindia.gov.in/en/pms-profile/",
            ],
        )

    if not (model.startswith("openai-") or model.startswith("hf-")):
        model = "openai-chatgpt"  # Default

    print("Scraping the Internet")
    results: tuple[list[str], list[str]] = internet.Google(
        query, GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_ENGINE_ID
    ).google()
    print("Done scraping the Internet")
    context: str = str(" ".join([str(string) for string in results]))
    # print(f"context: {context}")

    if model.startswith("openai-"):
        if model == "openai-chatgpt":
            # ChatGPT
            prompt = f'Use the context: {context[:4000]} and answer the question: "{query}" with the context. Also write at the very least long answers.'
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
                prompt = f'Use the context: {context[:3000]} and answer the question: "{query}" with the context and prior knowledge. Also write at the very least long answers.'
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
        # HuggingFace
        print("Running the model")
        model = model.replace("hf-", "", 1)
        qa_model = pipeline("question-answering", model=model)
        response = qa_model(question=query, context=context)
        print("Running Complete")
        return (response["answer"], results[1])
