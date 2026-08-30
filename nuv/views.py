from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Product
from .form import ProductForm

# ─── USER VIEWS ───────────────────────────────────────────

class DashboardView(ListView):          # was TemplateView — changed to ListView
    model = Product
    template_name = 'dashboard.html'
    context_object_name = 'data'        # keeps 'data' so dashboard.html loop works as-is

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

# ─── SELLER VIEWS ─────────────────────────────────────────

class SellerDashboardView(TemplateView):
    template_name = 'seller/dashboard.html'

class SellerProductsView(ListView):
    model = Product
    template_name = 'seller/products.html'
    context_object_name = 'products'

class SellerAddProductView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'seller/add_product.html'
    success_url = reverse_lazy('seller_products')

class SellerUpdateProductView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'seller/update_product.html'
    success_url = reverse_lazy('seller_products')