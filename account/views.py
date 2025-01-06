# views.py

from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model  # Import get_user_model

User = get_user_model()  # Retrieve the current user model

def home(request):
    return render(request, 'account/index.html')

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('my-login')

    context = {'RegisterForm': form}

    return render(request, 'account/register.html', context)

def my_login(request):
    users_exist = User.objects.exists()  # Check if any users are registered
    form = AuthenticationForm()

    if not users_exist:
        messages.info(request, "No accounts are currently registered. Please register first.")
        return redirect('register')  # Redirect to the registration page

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")

    context = {
        'LoginForm': form,
        'users_exist': users_exist  # Pass the users_exist flag to the template
    }

    return render(request, 'account/my-login.html', context)

def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('my-login')
