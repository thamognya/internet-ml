import json
import os

from dotenv import load_dotenv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .tools import question_answer

load_dotenv()
import internet_ml.NLP.no_context.QA


class QAView(APIView):
    def post(self, request, format=None):
        """
        {"question": "Who is Elon Musk?"}
        {
            "error": "",
            "response": {
                'score': VAL,
                'start': VAL,
                'end': VAL,
                'answer': 'THE_ANSWER'
            },
            "resources": [
                'SOME_LINKS_HERE'
            ]
        }
        or
        {
            "error": "",
            "status": "",
            "detail": "",
        }
        so check error if it exists first and then for other stuff
        """
        answer = internet_ml.NLP.no_context.QA.answer(
            request.POST.get("question"),
            str(os.getenv("INTERNET_ML_GOOGLE_API")),
            str(os.getenv("INTERNET_ML_GOOGLE_SEARCH_ENGINE_ID")),
        )
        content = json.dumps(
            {"error": "", "response": answer[0], "resources": answer[1]}
        )
        return content
