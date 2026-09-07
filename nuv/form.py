from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['p_title', 'p_price', 'p_description', 'qty', 'is_active', 'p_img']
        widgets = {
            'p_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. NAV Hoodie'}),
            'p_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'p_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'qty': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

    def clean_p_title(self):
        title = self.cleaned_data.get('p_title', '').strip()
        if not title:
            raise forms.ValidationError("Product title cannot be empty.")
        if len(title) < 3:
            raise forms.ValidationError("Product title must be at least 3 characters long.")
        return title

    def clean_p_price(self):
        price = self.cleaned_data.get('p_price')
        if price is None:
            raise forms.ValidationError("Price is required.")
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        if price > 99999999.99:
            raise forms.ValidationError("Price is unrealistically high.")
        return price

    def clean_p_description(self):
        description = self.cleaned_data.get('p_description', '').strip()
        if not description:
            raise forms.ValidationError("Please provide a product description.")
        if len(description) < 10:
            raise forms.ValidationError("Description must be at least 10 characters long.")
        return description

    def clean_qty(self):
        qty = self.cleaned_data.get('qty')
        if qty is None:
            raise forms.ValidationError("Quantity is required.")
        if qty < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return qty

    def clean_p_img(self):
        img = self.cleaned_data.get('p_img')
        if img:
            valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
            if not str(img.name).lower().endswith(valid_extensions):
                raise forms.ValidationError("Only JPG, JPEG, PNG, or WEBP image files are allowed.")
            if img.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file size must not exceed 5MB.")
        return img

    def clean(self):
        cleaned_data = super().clean()
        qty = cleaned_data.get('qty')
        is_active = cleaned_data.get('is_active')
        if is_active and qty == 0:
            self.add_error('is_active', "A product with zero quantity cannot be marked active. Set quantity or deactivate it.")
        return cleaned_data