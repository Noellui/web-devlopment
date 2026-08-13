from django.http import HttpResponse
from django.views.generic import TemplateView

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

class MenView(TemplateView):
    template_name = 'men.html'

class WomenView(TemplateView):
    template_name = 'women.html'

class HatsView(TemplateView):
    template_name = 'hats.html'

class AccessoriesView(TemplateView):
    template_name = 'accessories.html'