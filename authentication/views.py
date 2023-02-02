from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render(request, "authentication/index.html")

def register(request):
    if request.method == "POST":
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        username = request.POST['uname']
        email = request.POST['email']
        password = request.POST['pass']
        c_pass = request.POST['cpass']
        
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = first_name
        myuser.last_name = last_name
        
        myuser.save()
        
        messages.success(request, "Yaayy! Your Details Has Been Successfully Submitted. Check your email for verification.")
        
        return redirect('login')
    
    return render(request, "authentication/register.html")

def log_in(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pass']
        
        #Authenticate user
        user = authenticate(username=username, password=password) 
        
        if user is not None:
            login(request, user)
            first_name = user.first_name
            return render(request, "authentication/landing.html", {'first_name' : first_name} )
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
        
    return render(request, "authentication/login.html")

def log_out(request):
    logout(request)
    messages.success(request, "Logged out successfully :)")
    return redirect('home')

def landing(request):
    return render(request, "authentication/landing.html")
    