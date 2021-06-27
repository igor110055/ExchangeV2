from django.contrib import admin
from django.urls import path, include
from rest_framework import views
from . import views

urlpatterns = [
   path('staff' , views.staff.as_view() , name='staff'),
   path('bankcards' , views.bankcards.as_view() , name='bankcards'),
]
