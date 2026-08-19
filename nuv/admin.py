from django.contrib import admin
from . models import Product

class ProductAdmim(admin.ModelAdmin):
    list_display=("p_title",'p_price','p_description','is_active','qty','p_img_url')
admin.site.register(Product ,ProductAdmim)
# Register your models here.
