from django.urls import path
from nuv import views
from django.contrib import admin
urlpatterns = [
    path('', views.ProdectView.as_view(),name="dashboard"),
    path('men/', views.MenView.as_view(),name="men"),
    path('women/', views.WomenView.as_view(),name="women"),
    path('hats/', views.HatsView.as_view(),name="hats"),
    path('accessories/', views.AccessoriesView.as_view(),name="accessories"),
    path('admin/',admin.site.urls),
]