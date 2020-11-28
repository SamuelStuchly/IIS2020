from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'HotelApp/home.html')

def about(request):
    return render(request,'HotelApp/about.html')

@login_required
def edit(request):    
    return render(request, 'HotelApp/edit.html')

