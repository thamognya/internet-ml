from typing import Any

import concurrent.futures
import logging
import sys
from pathlib import Path

import nltk
import numpy as np
import spacy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# from scipy.spatial.distance import jaccard
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.append(str(Path(__file__).parent.parent.parent.parent) + "/utils/NLP")
sys.path.append(str(Path(__file__).parent.parent.parent.parent) + "/utils")

import config

logging.basicConfig(
    filename="relevancy.log",
    filemode="w",
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s",
)

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

nlp = spacy.load("en_core_web_sm")  # Load the English language model
lemmatizer = WordNetLemmatizer()  # Initialize the WordNet lemmatizer
stop_words = set(stopwords.words("english"))  # Get the English stop words


def jaccard(u: Any, v: Any) -> Any:
    # Pad the shorter array with zeros at the end
    u = np.pad(u, (0, max(u.shape[0], v.shape[0]) - u.shape[0]), "constant")
    v = np.pad(v, (0, max(u.shape[0], v.shape[0]) - v.shape[0]), "constant")
    # Calculate the Jaccard similarity
    nonzero = np.bitwise_or(u != 0, v != 0)
    intersection = np.bitwise_and(u != 0, v != 0)
    return 1.0 - float(np.count_nonzero(intersection)) / float(
        np.count_nonzero(nonzero)
    )


def is_answer(sentence: str, question: str, threshold: float = 0.3) -> bool:
    # Tokenize the sentence and the question
    sentence_tokens = word_tokenize(sentence)
    question_tokens = word_tokenize(question)
    # Remove stop words from the sentence and the question
    sentence_tokens = [
        token for token in sentence_tokens if token.lower() not in stop_words
    ]
    question_tokens = [
        token for token in question_tokens if token.lower() not in stop_words
    ]
    # Perform lemmatization on the sentence and the question
    sentence_tokens = [lemmatizer.lemmatize(token.lower()) for token in sentence_tokens]
    question_tokens = [lemmatizer.lemmatize(token.lower()) for token in question_tokens]
    # Extract the main verb from the question
    main_verb = None
    for token in question_tokens:
        if nlp(token)[0].pos_ == "VERB":
            main_verb = token
            break
    # Generate numerical representations of the sentence and the question using TF-IDF
    vectorizer = TfidfVectorizer()
    sentence_vector = vectorizer.fit_transform([sentence]).toarray()[0]
    question_vector = vectorizer.fit_transform([question]).toarray()[0]
    # Calculate the similarity between the sentence and the question
    similarity = 1 - jaccard(sentence_vector, question_vector)
    # Check if the sentence answers the question
    answer: bool
    if main_verb is None:
        answer = similarity >= threshold
    else:
        answer = main_verb in sentence_tokens and similarity >= threshold
    if config.CONF_DEBUG:
        logging.info(
            f"Is Relevant -> Sentence: {sentence}, Question: {question} -> Relevancy: {answer}"
        )
    return answer


def filter_irrelevant(sentences: list[str], question: str) -> list[str]:
    # Create a list to store the relevant sentences
    relevant_sentences = []
    for sentence in sentences:
        if is_answer(sentence, question):
            relevant_sentences.append(sentence)
            print(sentence)
    if config.CONF_DEBUG:
        logging.info(f"Relevant Sentences: {relevant_sentences}")
    return relevant_sentences


# # Test the is_answer function
# sentence = "Neil Armstrong was the first person to walk on the Moon."
# question = "Who was the first person to walk on the Moon?"
# if is_answer(sentence, question):
#     print("The sentence answers the question.")
# else:
#     print("The sentence does not answer the question.")

# from concurrent.futures import ThreadPoolExecutor
# import concurrent.futures

"""
print(
    filter_irrelevant(
        [
            "Neil Armstrong is an American Astronaut",
            "Neil Armstrong is dead",
            "Neil Armstrng is fake",
        ],
        "Who is Neil Armstrong?",
    )
)
"""
