from django.views.generic import TemplateView
from .models import Product
from django.shortcuts import render
from django.views.generic import ListView
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

class ProdectView(ListView):
    model = Product
    template_name='dashboard.html'
    context_object_name = 'data'