import json

from django.views.generic.base import TemplateView
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from internet_ml.NLP.no_context import QA

load_dotenv()


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
        try:
            answer = QA.answer(request.POST.get("question"))
            content = json.dumps(
                {"error": "", "response": answer[0], "resources": answer[1]}
            )
            return Response(content, status=status.HTTP_200_OK)
        except:
            content = json.dumps(
                {"error": "Google API key not present in .env or environment"}
            )
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
