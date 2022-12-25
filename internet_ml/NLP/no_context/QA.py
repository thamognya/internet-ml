import sys
from pathlib import Path

from transformers import pipeline

sys.path.append(str(Path(__file__).parent.parent.parent) + "/tools/NLP/data")
import internet

qa_model = pipeline("question-answering")
question = "Who is Elon Musk?"
a = internet.google(question)[0]
print(a)
context = ""
for i in a:
    context += str(i)
print(qa_model(question=question, context=context))
## {'answer': 'İstanbul', 'end': 39, 'score': 0.953, 'start': 31}
