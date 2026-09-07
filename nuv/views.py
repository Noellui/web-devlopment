from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Product
from .form import ProductForm


# ─── USER VIEWS ───────────────────────────────────────────

class DashboardView(ListView):
    model = Product
    template_name = 'dashboard.html'
    context_object_name = 'data'

class MenView(ListView):
    model = Product
    template_name = 'men.html'
    context_object_name = 'products'

class WomenView(ListView):
    model = Product
    template_name = 'women.html'
    context_object_name = 'products'

class AccessoriesView(ListView):
    model = Product
    template_name = 'accessories.html'
    context_object_name = 'products'

class HatsView(ListView):
    model = Product
    template_name = 'hats.html'
    context_object_name = 'products'


# ─── SELLER AUTH VIEWS ────────────────────────────────────

class SellerLoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('seller_dashboard')
        return render(request, 'seller/login.html')

    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)   
            return redirect('seller_dashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return render(request, 'seller/login.html')


class SellerLogoutView(View):

    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('seller_login')

class SellerDashboardView(LoginRequiredMixin, TemplateView):
    login_url = '/seller/login/'
    template_name = 'seller/dashboard.html'


class SellerProductsView(LoginRequiredMixin, ListView):
    login_url = '/seller/login/'
    model = Product
    template_name = 'seller/products.html'
    context_object_name = 'products'


class SellerAddProductView(LoginRequiredMixin, CreateView):
    login_url = '/seller/login/'
    model = Product
    form_class = ProductForm
    template_name = 'seller/add_product.html'
    success_url = reverse_lazy('seller_products')

    def form_valid(self, form):
        messages.success(self.request, f'"{form.instance.p_title}" was added successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please fix the errors below before saving.')
        return super().form_invalid(form)


class SellerUpdateProductView(LoginRequiredMixin, UpdateView):
    login_url = '/seller/login/'
    model = Product
    form_class = ProductForm
    template_name = 'seller/update_product.html'
    success_url = reverse_lazy('seller_products')
