import sys
from pathlib import Path

from transformers import pipeline

sys.path.append(str(Path(__file__).parent.parent.parent) + "/tools/NLP/data")
import internet

qa_model = pipeline("question-answering")
question = "Who is Rishi Sunak"
a = str(internet.google(question)[0])
print(qa_model(question=question, context=a))
## {'answer': 'İstanbul', 'end': 39, 'score': 0.953, 'start': 31}
