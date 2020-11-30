from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField




class Hotel(models.Model):
    name = models.CharField(max_length=100)
    stars = models.PositiveIntegerField()
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    description = models.TextField()
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # TODO: maybe add owner , ajked asi ne skor do owner class bude reference na owner a hotovo.

    def __str__(self):
        return self.name
    # 3 obrazky este 

    def get_absolute_url(self):
       return reverse('hotel-detail', kwargs={'pk': self.pk})

class Room(models.Model):
    ROOM_TYPES = (
        ('S', 'Single'),
        ('D', 'Double'),
        ('L', 'Large'),
        ('K', 'King'),
        ('T', 'Twin'),
    )
    room_type = models.CharField(max_length=1, choices=ROOM_TYPES, default='S')
    beds_number = models.PositiveIntegerField()
    price= models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    occupied = models.BooleanField(default=False)
    number = models.PositiveIntegerField()

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    # image = models.ImageField()
    # TODO: pridat obrazok polda typu izby a hotela


class Order(models.Model):
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateField(auto_now_add=True)
    
    # if user is registered
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    
    # if user is not registered
    name = models.CharField(max_length=100,blank=True)
    surname = models.CharField(max_length=100,blank=True)
    email = models.EmailField(blank=True) 
    phone = PhoneNumberField(blank=True)

    #TODO: sholtikovi povedat nech zmenime diagram

class Reservation(models.Model):
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    from_date = models.DateField()
    to_date = models.DateField()
    active = models.BooleanField(default=True)

    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    
    # TODO zmena do ER connection rezervace a user 




# Fake data 
'''
hilton = Hotel(name="Hilton",stars=5,address="Dlha 69",city="Bardejov",rating=4.3,description="Very nice hotel in great city, nice garden also, hotdog stand outside sucks tho.")
trump = Hotel(name="Trump",stars=4,address="Kratka ulica 3",city="Saca",rating=3.2,description="Not so good hotel in not so nice city, ugly garden also, hotdog stand outside very good tho.")
grand = Hotel(name="Hilton",stars=3,address="Pekna ulica 42",city="Bardejov",rating=4.9,description="Very cheap hotel in great city, no garden, hotdog stand outside mediocre.")

room1 = Room(type='S', beds_number=1,price=11.99,description="small room but very pretty, has TV also.", hotel=hilton)
room2 = Room(type='L', beds_number=4,price=50.99,description="large room but very pretty, has TV also and shower.", hotel=hilton)
room3 = Room(type='T', beds_number=2,price=23.99,description="twin beds room  very pretty, has TV also and closet.", hotel=hilton)

room4 = Room(type='S', beds_number=1,price=110.99,description="small room but very pretty, has TV also.", hotel=trump)
room5 = Room(type='L', beds_number=4,price=150.99,description="large room but very pretty, has TV also and shower.", hotel=trump)
room6 = Room(type='T', beds_number=2,price=123.99,description="twin beds room  very pretty, has TV also and closet.", hotel=trump)


room7 = Room(type='S', beds_number=1,price=3.99,description="small room but very pretty, has TV also.", hotel=grand)
room8 = Room(type='L', beds_number=4,price=6.99,description="large room but very pretty, has TV also and shower.", hotel=grand)

mylist = [hilton,trump,grand,room1,room2,room3,room4,room5,room6,room7,room8]
for i in mylist:
    i.save()
'''