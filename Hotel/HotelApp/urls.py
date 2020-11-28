from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='HotelApp-home'),
    path('edit/', views.edit, name='HotelApp-edit'),
    path('about/', views.about, name='HotelApp-about'),
]
