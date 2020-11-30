from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Hotel, Room, Reservation, Order
from .filters import HotelFilter,RoomFilter


# Create your views here.
# def home(request):
#     context = {
#         'Hotels': Hotel.objects.all()
#     }
#     return render(request,'HotelApp/home.html',context)


def about(request):
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

# class RoomListView(ListView):
#     model = Room
#     template_name = 'HotelApp/rooms_list.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'Rooms'
#     # ordering = ['-date_posted']
#     # chnaged

class RoomDetailView(DetailView):
    model = Room

    # def get_context_data(self, *args, **kwargs):
    #     context = super(RoomDetailView, self).get_context_data(*args, **kwargs)
    #     context['Rooms'] = Room.objects.filter(hotel=self.get_object())_
    #     return context


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


# # ======== Order views ========= #

# class OrderListView(ListView):
#     model = Order
#     template_name = 'OrderApp/home.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'Orders'
#     # ordering = ['-date_posted']
#     # chnaged

# class OrderDetailView(DetailView):
#     model = Order

# #TODO
# class OrderCreateView(LoginRequiredMixin, CreateView):
#     model = Order
#     fields = ['title', 'content']

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)


# #TODO
# class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Order
#     fields = ['title', 'content']

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

#     def test_func(self):
#         post = self.get_object()
#         if self.request.user == post.author:
#             return True
#         return False

# #TODO
# class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Order
#     success_url = '/'

#     def test_func(self):
#         post = self.get_object()
#         if self.request.user == post.author:
#             return True
#         return False

# # ======== RESERVATION views ========= #


# class ReservationListView(ListView):
#     model = Reservation
#     template_name = 'ReservationApp/home.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'Reservations'
#     # ordering = ['-date_posted']
#     # chnaged

# class ReservationDetailView(DetailView):
#     model = Reservation

# #TODO
# class ReservationCreateView(LoginRequiredMixin, CreateView):
#     model = Reservation
#     fields = ['title', 'content']

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)


# #TODO
# class ReservationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Reservation
#     fields = ['title', 'content']

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

#     def test_func(self):
#         post = self.get_object()
#         if self.request.user == post.author:
#             return True
#         return False

# #TODO
# class ReservationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Reservation
#     success_url = '/'

#     def test_func(self):
#         post = self.get_object()
#         if self.request.user == post.author:
#             return True
#         return False

# # ======== USERS views ========= #

# # TODO: should be in users.views 

