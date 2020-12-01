from django.shortcuts import render,redirect,reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView
)
from .models import Hotel, Room, Reservation, Order
from .filters import HotelFilter,RoomFilter, OrderFilter, ReservationFilter
from users.forms import CustomUserCreationForm
from users.models import CustomUser


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
    fields = ['name', 'stars', 'rating', 'address', 'city', 'description']

    def form_valid(self, form):
        
        form.instance.owner = self.request.user
        return super().form_valid(form)



class HotelUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Hotel
    fields = ['name', 'stars', 'address', 'city', 'description','owner']
    

    def form_valid(self, form):
        # form.instance.owner = self.request.user 
        return super().form_valid(form)

    def test_func(self):
        hotel = self.get_object()
        if self.request.user.is_superuser or self.request.user == hotel.owner:
            return True
        return False


class HotelDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Hotel
    success_url = '/'

    def test_func(self):
        hotel = self.get_object()
        if self.request.user.is_superuser or self.request.user == hotel.owner:
            return True
        return False

# ======== ROOM views ========= #


class RoomDetailView(DetailView):
    model = Room

#TODO
class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    fields = ['number','room_type', 'beds_number', 'price' , 'description']

    def form_valid(self, form):
        form.instance.hotel = Hotel.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('hotel-detail',kwargs=self.kwargs )


#TODO
class RoomUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Room
    fields = ['number','room_type', 'beds_number', 'price' , 'description', 'occupied']

    def form_valid(self, form):
        # form.instance.hotel.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        room = self.get_object()
        print(room)
        if self.request.user.is_superuser or self.request.user == room.hotel.owner:
            return True
        return False

#TODO
class RoomDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Room
    success_url = '/'

    def test_func(self):
        room = self.get_object()
        if self.request.user.is_superuser or self.request.user == room.hotel.owner:
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


class ReservationCreateView( CreateView,FormView):
    model = Reservation
    fields = ['from_date', 'to_date' ]
 

    def form_valid(self, form):
        from_date = form.instance.from_date 
        to_date = form.instance.to_date 
        form.instance.room = Room.objects.get(pk=self.kwargs['id'])
        form.instance.price = form.instance.room.price
        if self.request.user.is_authenticated:
            order_qs = Order.objects.filter(user=self.request.user,active=False)
            if order_qs.exists():
                order = order_qs[0]
                print("TYP",type(order))
                print("TYP",type(order.active))
                if order.user == self.request.user and not order.active:
                    form.instance.order = order
                    return super().form_valid(form)
            else:
                price = self.calculate_price(form.instance.room,from_date,to_date)
                deposit = price * 0.3
                print("VYTVARAM OBEJDNAVKU")
                
                form.instance.order = Order.objects.create(price=price,deposit=deposit,user=self.request.user,active=False)
                # order.save()
        else:
            price = self.calculate_price(form.instance.room,from_date,to_date)
            deposit = price * 0.3
            print("VYTVARAM OBEJDNAVKU")
            
            form.instance.order = Order.objects.create(price=price,deposit=deposit,active=False)


        return super().form_valid(form)
    
    def get_success_url(self):
            print("IDEM NA SUCCES URL ")
            return reverse('order-detail',kwargs={'pk':self.kwargs['pk']})
    
    

    def calculate_price(self,room,date1,date2):
        days_num = date2-date1
        price = float(room.price) * int(days_num.days)
        return price


class ReservationDeleteView( UserPassesTestMixin, DeleteView):
    model = Reservation

    def test_func(self):
        res = self.get_object()
        if self.request.user.is_staff or self.request.user == res.order.user:
            return True
        return False

    def get_success_url(self):
           print("IDEM NA SUCCES URL ")
           return reverse('order-detail',kwargs={'pk':self.kwargs['pk']})



class OrderFinishRegisteredView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Order
    template_name = 'HotelApp/order_registered_finish.html' 

    def test_func(self):
        return True

  
    def get_success_url(self):
           return reverse('order-succes')




class OrderFinishUnRegisteredView(UserPassesTestMixin, UpdateView):
    model = Order
    template_name = 'HotelApp/order_unregistered_finish.html' 

    fields = ['name','username','email']
    form_class=CustomUserCreationForm

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        order= self.get_object()
        users = CustomUser.objects.all()
        email_list=[]
        for i in users: 
            email_list.append(i.email)
        if order.email not in email_list:
            return True
        return False

    def get_success_url(self):
            print("IDEM NA SUCCES URL ")
            order= self.get_object()
            activate_order(order)
            return reverse('order-success',kwargs={'pk':self.kwargs['pk']})

def activate_order(order):
    order.active = True
    order.save()



class OrderDeleteView( UserPassesTestMixin, DeleteView):
    model = Order

    def test_func(self):
        order = self.get_object()
        if self.request.user.is_staff or self.request.user == order.user:
            return True
        return False

    def get_success_url(self):
           print("IDEM NA SUCCES URL ")
           return reverse('order-list')

def success(request):
    return render(request,'HotelApp/success.html')