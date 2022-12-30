from django.views.generic.base import TemplateView


class APIView(TemplateView):
    template_name = "index.api.dj.html"
