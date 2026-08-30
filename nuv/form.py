from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['p_title', 'p_price', 'p_description', 'qty', 'is_active', 'p_img']