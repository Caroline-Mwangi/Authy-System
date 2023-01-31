from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

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
        
        messages.success(request, "Yaayy! Your Account Has Been Successfully Created.")
        
        return redirect('login')
    
    return render(request, "authentication/register.html")

def login(request):
    return render(request, "authentication/login.html")

def logout(request):
    pass