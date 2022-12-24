import datasets
from typing import Any

CoQA: Any = datasets.load_dataset("coqa")
DATASET: List[Any] = []

def coqa():
    global CoQA, DATASET
    for story in CoQA["train"]:
        for question, answer in story["questions"], story["answers"]:
            