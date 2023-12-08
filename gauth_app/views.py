from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def user_signup(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            new_customer = form.save(commit=False)
            new_customer.username = form.cleaned_data['email']
            new_customer.save()

            login(request, new_customer)
            messages.success(request, "Registration successful.")
            return redirect("gauth_app:user_login")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()
    return render(request=request, template_name="main/signup.html", context={"register_form": form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')  
            password = form.cleaned_data.get('password') 
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("main_app:home")
            else:
                messages.error(request, "Invalid username or password. Please check your credentials.")
        else:
            messages.error(request, "Invalid form submission. Please check your input.")
    else:
        form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"login_form": form})