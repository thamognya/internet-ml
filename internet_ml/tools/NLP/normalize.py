import logging

# logging config
logging.basicConfig(
    filename="normalize.log",
    filemode="w",
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s",
)

import concurrent.futures
import string
import sys
from pathlib import Path

import contractions
import tokenizers
from tokenizers.normalizers import NFKD, Lowercase, Strip, StripAccents

# Add utils directory to path
sys.path.append(str(Path(__file__).parent.parent.parent) + "/utils/NLP")
sys.path.append(str(Path(__file__).parent.parent.parent) + "/utils")
import config

# Define normalization sequence
NORMALIZER_SEQ: tokenizers.normalizers.Sequence = tokenizers.normalizers.Sequence(
    [Lowercase(), NFKD(), Strip(), StripAccents()]
)


def remove_non_ascii(string: str) -> str:
    return string.encode("ascii", errors="ignore").decode()


def normalizer(text: str) -> str:
    global remove_non_ascii
    """Normalize input text.

    Args:
        text (str): Input text to normalize.

    Returns:
        str: Normalized text.
    """
    global NORMALIZER_SEQ
    # Expand contractions
    contractions.fix(text)
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Normalize string
    text = NORMALIZER_SEQ.normalize_str(text)
    text = (
        text.replace("\n", " ")
        .replace("\t", " ")
        .replace("\r", " ")
        .replace("'", " ")
        .replace("\\x", " ")
        .replace('"', " ")
        .replace("\\", " ")
        .replace("\\", " ")
        .replace("\\r", " ")
        .replace("\\f", " ")
        .replace("\\a", " ")
        .replace(r"\/a", " ")
        .replace(r"\/f", " ")
        .replace(r"\/b", " ")
        .replace("               ", " ")
    )
    text = remove_non_ascii(text)
    if config.CONF_DEBUG:
        logging.info(text)
    return text


def normalize_sentences(sentences: list[str]) -> list[str]:
    normalized_sentences = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(normalizer, sentence) for sentence in sentences]
        for future, sentence in zip(
            concurrent.futures.as_completed(futures), sentences
        ):
            if future.result():
                normalized_sentences.append(sentence)
    if config.CONF_DEBUG:
        logging.info(f"Normalized Sentences: {normalize_sentences}")
    return normalized_sentences
