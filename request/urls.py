from django.urls import path
from . import views

urlpatterns = [
    path('deposit/', views.deposit),
    path('withdraw/', views.withdraw),
    path('pair_price/', views.pair_price),
    # path('api/v1/request/currencies/', views.currencies),
]