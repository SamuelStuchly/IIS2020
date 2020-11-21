from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home,name='HotelApp-home'),
    path('about/', views.about,name='HotelApp-about'),
]
