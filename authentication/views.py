from django.shortcuts import render

def home(request):
    return render(request, "authentication/index.html")

def register(request):
    return render(request, "authentication/register.html")

def login(request):
    return render(request, "authentication/login.html")

def logout(request):
    pass