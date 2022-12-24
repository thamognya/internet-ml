# mypy: ignore-errors
# checks if sentence is relevant to other sentence
from typing import List

import concurrent.futures
import pickle

import spacy

# Load the English language model
NLP = spacy.load("en_core_web_sm")
from pathlib import Path

CACHE_FILE_PATH: str = "./is_relevant_cache.pkl"

try:
    with open(CACHE_FILE_PATH, "rb") as f:
        cache = pickle.load(f)
except (OSError, EOFError):
    cache = {}


def is_relevant(sentence: str, question: str) -> bool:
    global NLP

    cache_key = (sentence, question)
    if cache_key in cache:
        relevant: bool = cache[cache_key]
        return relevant
    # Process the sentence and question
    doc_sentence = NLP(sentence)
    doc_question = NLP(question)

    # Extract the named entities and important words or phrases from the sentence
    sentence_important = {
        token.text
        for token in doc_sentence
        if token.pos_ in ["NOUN", "PROPN", "ADJ"] or token.ent_type_ != ""
    }
    question_important = {
        token.text
        for token in doc_question
        if token.pos_ in ["NOUN", "PROPN", "ADJ"] or token.ent_type_ != ""
    }

    # Check if any of the named entities or important words or phrases in the question are in the sentence
    for token in question_important:
        if token in sentence_important:
            cache[cache_key] = True
            with open(CACHE_FILE_PATH, "wb") as f:
                pickle.dump(cache, f)
            return True

    # Check if the sentence contains any negative words
    for token in doc_sentence:
        if token.pos_ == "ADV" and token.dep_ == "neg":
            cache[cache_key] = False
            with open(CACHE_FILE_PATH, "wb") as f:
                pickle.dump(cache, f)
            return False

    cache[cache_key] = False
    with open(CACHE_FILE_PATH, "wb") as f:
        pickle.dump(cache, f)
    return False


def filter_irrelevant(sentences: list[str], question: str) -> list[str]:
    relevant_sentences = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(is_relevant, sentence, question) for sentence in sentences
        ]
        for future, sentence in zip(
            concurrent.futures.as_completed(futures), sentences
        ):
            if future.result():
                relevant_sentences.append(sentence)
    return relevant_sentences


# print(filter_irrelevant(["jeff bezos died", "jeff is stupid", "jeff bezos is an entrepenur"], "who is jeff bezos"))
