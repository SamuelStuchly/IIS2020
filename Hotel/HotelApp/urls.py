from django.urls import path 
from . import views
from .views import (
    HotelListView,
    HotelDetailView,
    HotelCreateView,
    HotelUpdateView,
    HotelDeleteView,
    
    RoomDetailView,
    RoomCreateView,
    RoomUpdateView,
    RoomDeleteView
    
)

urlpatterns = [
    path('', HotelListView.as_view(),name='HotelApp-home'),
    path('hotel/<int:pk>/', HotelDetailView.as_view(), name='hotel-detail'),
    path('room/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('hotel/new/', HotelCreateView.as_view(), name='hotel-create'),
    path('room/new/', RoomCreateView.as_view(), name='room-create'),
    path('hotel/<int:pk>/update/', HotelUpdateView.as_view(), name='hotel-update'),
    path('room/<int:pk>/update/', RoomUpdateView.as_view(), name='room-update'),
    path('hotel/<int:pk>/delete/', HotelDeleteView.as_view(), name='hotel-delete'),
    path('room/<int:pk>/delete/', RoomDeleteView.as_view(), name='room-delete'),
    path('about/', views.about,name='HotelApp-about'),
]
