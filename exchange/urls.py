from django.contrib import admin
from django.urls import path, include
from rest_framework import views
from . import views

urlpatterns = [
   path('userinfo' , views.usersinfo.as_view() , name='userinfo'),
   path('user' , views.user.as_view() , name='user'),
   path('wallet' , views.wallets.as_view() , name='wallet'),
   path('wallet/<int:id>' , views.wallet.as_view() , name='wallets'),
   path('currencies' , views.currencies.as_view() , name='Currencies'),
   path('currencies/<int:id>' , views.currency.as_view() , name='currency'),
   path('verify' , views.verify.as_view() , name='Verify'),
   path('bankcards' , views.bankcards.as_view() , name='bankcards'),
   path('bankaccounts' , views.bankaccounts.as_view() , name='bankaccounts'),
   path('transactions' , views.transactions.as_view() , name='transactions'),
   path('settings' , views.settings.as_view() , name='settings'),
   path('subjects' , views.subjects.as_view() , name='subjects'),
   path('tickets/<int:subject>' , views.tickets.as_view() , name='tickets'),
   path('pages' , views.pages.as_view() , name='pages'),
   path('forget' , views.addforget.as_view() , name='addforget'),
   path('resetpass/<uuid:key>' , views.resetpass.as_view() , name='resetpass'),
   path('resetpass' , views.resetpass.as_view() , name='resetpass'),
   path('mobile-verify' , views.mobileverify.as_view() , name='mobileverify'),
   path('mobile-verify/<str:number>' , views.mobileverify.as_view() , name='mobileverify'),
   path('email-verify' , views.emailverify.as_view() , name='emailverify'),
   path('bsc' , views.bsc.as_view() , name='bsc'),
   path('price' , views.price.as_view() , name='price'),
]
