from django.views.generic.base import TemplateView

# Create your views here.


class QAView(TemplateView):
    template_name = "index.question_answer.dj.html"
