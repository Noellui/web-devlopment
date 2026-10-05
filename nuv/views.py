from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.generic import (CreateView, FormView, ListView,TemplateView, UpdateView)
from .auth_forms import SellerLoginForm, SellerRegistrationForm
from .form import ProductForm
from .models import Product


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


# ─── ACCESS CONTROL MIXINS ────────────────────────────────

class SellerRequiredMixin(LoginRequiredMixin):
    """Unauthenticated users are redirected to the seller login page (?next= is kept)."""
    login_url = reverse_lazy('seller_login')
    redirect_field_name = 'next'


class AnonymousOnlyMixin:
    """Logged-in sellers are bounced to the dashboard (login / register pages)."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('seller_dashboard')
        return super().dispatch(request, *args, **kwargs)


# ─── SELLER AUTH VIEWS ────────────────────────────────────

class SellerRegisterView(AnonymousOnlyMixin, FormView):
    template_name = 'seller/register.html'
    form_class = SellerRegistrationForm
    success_url = reverse_lazy('seller_login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Registration successful. Please sign in.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class SellerLoginView(AnonymousOnlyMixin, FormView):
    template_name = 'seller/login.html'
    form_class = SellerLoginForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        nxt = self.request.POST.get('next') or self.request.GET.get('next')
        if nxt and url_has_allowed_host_and_scheme(nxt, {self.request.get_host()},
                                                   self.request.is_secure()):
            return nxt
        return reverse_lazy('seller_dashboard')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(self.get_success_url())


class SellerLogoutView(View):
    """POST-only logout (prevents CSRF logout via a plain link/image)."""

    def post(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('seller_login')

    def get(self, request):
        return redirect('seller_dashboard' if request.user.is_authenticated else 'seller_login')


# ─── PROTECTED SELLER VIEWS ───────────────────────────────

class SellerDashboardView(SellerRequiredMixin, TemplateView):
    template_name = 'seller/dashboard.html'


class SellerProductsView(SellerRequiredMixin, ListView):
    model = Product
    template_name = 'seller/products.html'
    context_object_name = 'products'


class SellerAddProductView(SellerRequiredMixin, CreateView):
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


class SellerUpdateProductView(SellerRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'seller/update_product.html'
    success_url = reverse_lazy('seller_products')

    def form_valid(self, form):
        messages.success(self.request, f'"{form.instance.p_title}" was updated successfully.')
        return super().form_valid(form)