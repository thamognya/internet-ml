from QA import answer

print(
    answer(
        query="When was the last cricket worldcup held?",
        model="hf-deepset/roberta-large-squad2",
    )
)
