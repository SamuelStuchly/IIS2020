from django.urls import path 
from . import views
from users.views import createnew
from .views import (
    HotelListView,
    HotelDetailView,
    HotelCreateView,
    HotelUpdateView,
    HotelDeleteView,
    
    RoomDetailView,
    RoomCreateView,
    RoomUpdateView,
    RoomDeleteView,

    OrderListView,
    OrderDetailView,
    OrderDeleteView,
    
    ReservationCreateView,
    ReservationDeleteView,
    OrderFinishRegisteredView,
    OrderFinishUnRegisteredView
    

    
)
from users.views import (
    UserListView,
    UserDetailView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView
)


urlpatterns = [
    path('', HotelListView.as_view(),name='HotelApp-home'),
    path('customuser/', UserListView.as_view(), name='customuser'),
    path('customuser/<int:pk>/', UserDetailView.as_view(), name='customuser-detail'),
    path('customuser/new/', createnew, name='customuser-create'),
    path('customuser/<int:pk>/update', UserUpdateView.as_view(), name='customuser-update'),
    path('customuser/<int:pk>/delete', UserDeleteView.as_view(), name='customuser-delete'),
    
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('hotel/<int:pk>/', HotelDetailView.as_view(), name='hotel-detail'),
    path('hotel/<int:pk>/room/<int:id>/', RoomDetailView.as_view(), name='room-detail'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('hotel/new/', HotelCreateView.as_view(), name='hotel-create'),
    path('hotel/<int:pk>/room/new/', RoomCreateView.as_view(), name='room-create'),
    path('hotel/<int:pk>/update/', HotelUpdateView.as_view(), name='hotel-update'),
    path('hotel/<int:pk>/room/<int:id>/update/', RoomUpdateView.as_view(), name='room-update'),
    path('hotel/<int:pk>/delete/', HotelDeleteView.as_view(), name='hotel-delete'),
    path('hotel/<int:pk>/room/<int:id>/delete/', RoomDeleteView.as_view(), name='room-delete'),
    
    # path('order/create/', create_order ,name='order-create'),
    path('order/delete/', OrderDeleteView.as_view() ,name='order-delete'),
    path('hotel/<int:pk>/room/<int:id>/res/add/', ReservationCreateView.as_view() ,name='res-add'),
    path('hotel/<int:pk>/room/<int:id>/res<int:r_id>/delete/', ReservationDeleteView ,name='res-delete'),

    path('order/<int:pk>/registered/finish/', OrderFinishRegisteredView.as_view(), name='order-finish-registered'),
    path('order/<int:pk>/unregistered/finish/', OrderFinishUnRegisteredView.as_view(), name='order-finish-unregistered'),
    path('about/', views.about,name='HotelApp-about'),
    path('success/', views.success,name='HotelApp-about'),
]
