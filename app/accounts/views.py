from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ProfileForm
from .models import Profile

def home(request):
    return render(request, 'fitlog/home.html')

def user_home(request):
    return render(request, 'fitlog/user_home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile_completion')
    else:
        form = SignUpForm()
    return render(request, 'fitlog/signup.html', {'form': form})

def profile_completion(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('user_home')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'fitlog/profile_completion.html', {'profile_form': profile_form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_home')
    else:
        form = AuthenticationForm()
    return render(request, 'fitlog/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_home')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'fitlog/edit_profile.html', {'form': form})