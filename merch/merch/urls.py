from django.urls import path
from nuv import views
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('men/', MenView.as_view(), name='men'),
    path('women/', WomenView.as_view(), name='women'),
    path('hats/', HatsView.as_view(), name='hats'),
    path('accessories/', AccessoriesView.as_view(), name='accessories'),
]