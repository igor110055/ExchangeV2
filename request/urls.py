from django.urls import path
from . import views

urlpatterns = [
    path('deposit/', views.deposit),
    path('withdraw/', views.withdraw),
    path('pair_price/', views.pair_price),
    path('deposit_success/<str:payment_id>', views.handle_success),
    path('commision/', views.commision),
    # path('api/v1/request/currencies/', views.currencies),
]