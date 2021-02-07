from django.views import View
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib import messages 
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

class Register(View):
    
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            username.capitalize()
            messages.success(request, f'Account created. Please Log In.')
            return redirect(reverse_lazy('login'))
        return render(request, "register/register.html", {'form': form})
        
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('main:home'))
        form = UserRegisterForm()
        return render(request,'register/register.html',{'form':form})

@login_required
def profile(request):

    if request.method=='POST':
        u_update_form = UserUpdateForm(request.POST, instance=request.user)
        p_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    
        if u_update_form.is_valid() and p_update_form.is_valid():
            u_update_form.save()
            p_update_form.save()
            messages.success(request, f'Your account has been updated.')
            return redirect('profile')
    else:
        u_update_form = UserUpdateForm(instance=request.user)
        p_update_form = ProfileUpdateForm(instance=request.user.profile)

    ctx = {
        'u_update_form': u_update_form,
        'p_update_form': p_update_form,
    }
    
    return render(request, 'register/profile.html',ctx)
