from django.views.generic.base import TemplateView


class NLPView(TemplateView):
    template_name = "index.api.nlp.dj.html"
