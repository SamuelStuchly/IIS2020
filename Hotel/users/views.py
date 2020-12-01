from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .filters import UserFilter 


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'users/customuser.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'CustomUser'

    def get_context_data(self, *args, **kwargs):
        context = super(UserListView, self).get_context_data(*args, **kwargs)
        context['filter'] = UserFilter(self.request.GET, queryset=self.get_queryset())
        print(context)
        return context

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:        
            return False



class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = CustomUser

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:        
            return False
    

#TODO:permissons vsade 
class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CustomUser
    fields = ['email']

    # TODO heslo na prihlasovanie


    """
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    """
    
    success_url = "/"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:        
            return False


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    fields = ['email', 'is_staff', 'is_owner', 'is_superuser']
    
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:        
            return False
    

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CustomUser
    success_url = '/'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False 


@login_required
def createnew(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Acount has been created.')
            return redirect('customuser')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/customuser_create.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Acount has been created. Ready to Log in !')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Profile updated!')
            return redirect('profile')        
    else:
        form = CustomUserChangeForm()

    return render(request, 'users/profile.html', { 'form': form })    