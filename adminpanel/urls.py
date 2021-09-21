from django.contrib import admin
from django.urls import path, include
from rest_framework import views
from . import views

urlpatterns = [
   path('staff' , views.staff.as_view() , name='staff'),
   path('subject' , views.subject.as_view() , name='subject'),
   path('subject/<int:id>' , views.subject.as_view() , name='subject'),
   path('ticket' , views.ticket.as_view() , name='ticket'),
   path('ticket/<int:id>' , views.ticket.as_view() , name='ticket'),
   path('bankcards' , views.bankcards.as_view() , name='bankcards'),
   path('bankaccounts' , views.bankaccounts.as_view() , name='bankaccounts'),
   path('verifymelli' , views.verifymelli.as_view() , name='verifymelli'),
   path('cwithdraw' , views.cwithdraw.as_view() , name='cwithdraw'),
   path('rcwithdraw' , views.rcwithdraw.as_view() , name='rcwithdraw'),
   path('ccwithdraw' , views.ccwithdraw.as_view() , name='ccwithdraw'),
   path('perpetualreq' , views.perpetualreq.as_view() , name='perpetualreq'),
   path('perpetualreqccept' , views.perpetualreqccept.as_view() , name='perpetualreqccept'),
   path('perpetualreq/<int:id>' , views.perpetualreq.as_view() , name='perpetualreq'),
   path('general' , views.general.as_view() , name='general'),
   path('user' , views.user.as_view() , name='user'),
]
