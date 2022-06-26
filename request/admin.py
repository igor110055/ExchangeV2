from pyexpat import model
from django.contrib import admin
from .models import WithdrawRequest, DepositRequest
# Register your models here.

@admin.register(WithdrawRequest)
class RequestAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "currency", "amount", "coin_amount", "address", "memo", ]

@admin.register(DepositRequest)
class RequestAdmin2(admin.ModelAdmin):
    list_display = ["id", "user", "currency", "amount",  "url" ]
    
