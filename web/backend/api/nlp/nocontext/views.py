import os

import dotenv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import internet_ml.NLP.no_context.QA

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
dotenv.load_dotenv(dotenv_path)


class QAView(APIView):
    def post(self, request):
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
            str(request.data["question"]),
            str(os.environ.get("GOOGLE_SEARCH_API_KEY")),
            str(os.environ.get("GOOGLE_SEARCH_ENGINE_ID")),
            str(os.environ.get("OPENAI_API_KEY")),
        )
        content = {
            "error": "",
            "question": str(request.data["question"]),
            "response": answer[0],
            "resources": answer[1],
        }
        return Response(content)
