from django.http import HttpResponse
from django.views.generic import TemplateView

from django.views.generic import TemplateView

class DashboardView(TemplateView):
    template_name = 'store/dashboard.html'

class MenView(TemplateView):
    template_name = 'store/men.html'

class WomenView(TemplateView):
    template_name = 'store/women.html'

class HatsView(TemplateView):
    template_name = 'store/hats.html'

class AccessoriesView(TemplateView):
    template_name = 'store/accessories.html'