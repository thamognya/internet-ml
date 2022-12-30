from typing import Any

import json

import internet_ml.NLP.no_context.QA


def QA(
    query: str, INTERNET_ML_GOOGLE_API: str, INTERNET_ML_GOOGLE_SEARCH_ENGINE_ID: str
) -> Any:
    try:
        answer = internet_ml.NLP.no_context.QA.answer(
            query, INTERNET_ML_GOOGLE_API, INTERNET_ML_GOOGLE_SEARCH_ENGINE_ID
        )
        content = json.dumps(
            {"error": "", "response": answer[0], "resources": answer[1]}
        )
    except:
        content = json.dumps(
            {"error": "Google API key not present in .env or environment"}
        )
    return content


# print(QA("Who is Elon Musk?"))
