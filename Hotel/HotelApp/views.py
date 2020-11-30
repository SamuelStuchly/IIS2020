from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Hotel, Room, Reservation, Order
from .filters import HotelFilter,RoomFilter, OrderFilter, ReservationFilter


def about(request):
    print(request)
    return render(request,'HotelApp/about.html')


# ======== HOTEL views ========= #

class HotelListView(ListView):
    model = Hotel
    template_name = 'HotelApp/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'Hotels'

    def get_context_data(self, *args, **kwargs):
        context = super(HotelListView, self).get_context_data(*args, **kwargs)
        context['filter'] = HotelFilter(self.request.GET,queryset=self.get_queryset())
        print(context)
        return context

class HotelDetailView(DetailView):
    model = Hotel

    def get_context_data(self, *args, **kwargs):
        context = super(HotelDetailView, self).get_context_data(*args, **kwargs)
        context['Rooms'] = Room.objects.filter(hotel=self.get_object())
        context['filter'] = RoomFilter(self.request.GET,queryset=context["Rooms"])
        print(self.get_queryset())
        print(context["Rooms"])
        return context


#TODO:permissons vsade 
class HotelCreateView(LoginRequiredMixin, CreateView):
    model = Hotel
    fields = ['name', 'stars', 'address', 'city', 'description']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)



class HotelUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Hotel
    fields = ['name', 'stars', 'address', 'city', 'description']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        hotel = self.get_object()
        if self.request.user == hotel.owner:
            return True
        return False


class HotelDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Hotel
    success_url = '/'

    def test_func(self):
        hotel = self.get_object()
        if self.request.user == hotel.owner:
            return True
        return False

# ======== ROOM views ========= #


class RoomDetailView(DetailView):
    model = Room

#TODO
class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    fields = ['number','room_type' 'beds_number', 'price' , 'description', 'occupied']

    def form_valid(self, form):
        form.instance.hotel.owner = self.request.user
        return super().form_valid(form)


#TODO
class RoomUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Room
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.hotel.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        room = self.get_object()
        if self.request.user == room.hotel.owner:
            return True
        return False

#TODO
class RoomDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Room
    success_url = '/'

    def test_func(self):
        room = self.get_object()
        if self.request.user == room.hotel.owner:
            return True
        return False


## ======== Order views ========= #


class OrderListView(ListView):
    model = Order
    # template_name = 'users/order_list.html'  # <app>/<model>_<viewtype>.html
    # context_object_name = 'Orders'

    def get_context_data(self, *args, **kwargs):
        context = super(OrderListView, self).get_context_data(*args, **kwargs)
        context['filter'] = OrderFilter(self.request.GET,queryset=self.get_queryset())
        print(context)
        return context

class OrderDetailView(DetailView):
    model = Order

    def get_context_data(self, *args, **kwargs):
        context = super(OrderDetailView, self).get_context_data(*args, **kwargs)
        context['Reservations'] = Reservation.objects.filter(order=self.get_object())
        print(self.get_queryset())
        return context


def add_reservation(request,order):
    

    return redirect('order-list')   


def remove_reservation(request,res):
    

    return redirect('order-list')   


def create_order(request,res):
    
    return redirect('order-list')   

def remove_order(request,order):

    return redirect('order-list')   