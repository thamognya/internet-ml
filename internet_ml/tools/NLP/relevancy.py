from typing import List

import concurrent.futures
import re


def filter_relevant(sentences: list[str], question: str) -> list[str]:
    def is_relevant(sentence: str) -> bool:
        # Use regular expression to check if the sentence contains any of the words in the question
        return bool(
            re.search(r"\b" + "\\b|\\b".join(question.split()) + r"\b", sentence)
        )

    # Create a thread pool with 4 worker threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
        # Map the is_relevant function to each sentence in the list and return the resulting list of booleans
        relevant = list(executor.map(is_relevant, sentences))

    # Return only the sentences where is_relevant returned True
    return [sentence for sentence, relevant in zip(sentences, relevant) if relevant]


# # Example usage
# context = ["The quick brown fox jumps over the lazy dog.", "The slow green snake slithers under the rock."]
# question = "quick brown fox"
# relevant_context = filter_relevant_context(context, question)
# print(relevant_context)  # Output: ["The quick brown fox jumps over the lazy dog."]
