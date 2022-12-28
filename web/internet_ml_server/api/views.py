from django.views.generic.base import TemplateView

# Create your views here.


class ApiView(TemplateView):
    template_name = "index.api.dj.html"
