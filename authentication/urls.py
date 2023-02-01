from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('login', views.log_in, name="login"),
    path('logout', views.log_out, name="logout"),
    path('landing', views.landing, name="landing"),
]