from QA import answer

print(
    answer(
        query="What is Legend of Zelda tears of the kingdom?",
        model="openai-chatgpt",
    )
)
# openai-chatgpt - 89.37%
# hf-deepset/roberta-large-squad2 - 85.67%
# hf-deepset/deberta-v3-large-squad2 - 82.56%
