from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from nuv import views
from django.contrib import admin

urlpatterns = [
    # ─── User URLs ───────────────────────────────────────
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('men/', views.MenView.as_view(), name='men'),
    path('women/', views.WomenView.as_view(), name='women'),
    path('hats/', views.HatsView.as_view(), name='hats'),
    path('accessories/', views.AccessoriesView.as_view(), name='accessories'),

    # ─── Seller Auth URLs ────────────────────────────────
   path('seller/register/', views.SellerRegisterView.as_view(), name='seller_register'),
   path('seller/login/',    views.SellerLoginView.as_view(),    name='seller_login'),
   path('seller/logout/',   views.SellerLogoutView.as_view(),   name='seller_logout'),

    # ─── Seller Protected URLs ───────────────────────────
    path('seller/', views.SellerDashboardView.as_view(), name='seller_dashboard'),
    path('seller/products/', views.SellerProductsView.as_view(), name='seller_products'),
    path('seller/add/', views.SellerAddProductView.as_view(), name='seller_add_product'),
    path('seller/update/<int:pk>/', views.SellerUpdateProductView.as_view(), name='seller_update_product'),

    path('admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
