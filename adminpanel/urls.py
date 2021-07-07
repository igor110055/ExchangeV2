from django.contrib import admin
from django.urls import path, include
from rest_framework import views
from . import views

urlpatterns = [
   path('staff' , views.staff.as_view() , name='staff'),
   path('bankcards' , views.bankcards.as_view() , name='bankcards'),
   path('bankaccounts' , views.bankaccounts.as_view() , name='bankaccounts'),
   path('verifymelli' , views.verifymelli.as_view() , name='verifymelli'),
   path('bankrequests' , views.bankrequests.as_view() , name='bankrequests'),
]
