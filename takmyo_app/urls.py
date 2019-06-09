from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('join/', views.join),
    path('join/check_id_duplicate/<str:user_id>/', views.check_id_duplicate),
    path('login/', views.my_login),
]