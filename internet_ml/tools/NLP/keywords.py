from typing import List

import spacy


def get_keywords(query: str) -> list[str]:
    # Load the NLP model
    nlp = spacy.load("en_core_web_sm")
    # Process the query
    doc = nlp(query)
    # Extract the nouns and adjectives from the query
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "ADJ"]]
    return keywords
