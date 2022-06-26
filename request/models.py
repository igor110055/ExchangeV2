from pyexpat import model
from tabnanny import verbose
from tkinter.tix import Tree
from webbrowser import get
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class WithdrawRequest(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    currency = models.CharField(max_length=255, verbose_name="Currency")
    amount = models.DecimalField(verbose_name="Amount in usd",max_digits=10,decimal_places=4, null=True, blank=True)
    coin_amount = models.IntegerField(verbose_name="Amount in currency", null=True, blank=True)
    address = models.CharField(max_length=60, verbose_name="Deposit address")
    memo = models.CharField(max_length=60, verbose_name="Address MEMO", blank=True)
    recipient_name = models.CharField(max_length=55, verbose_name="Recipient name")
    recipient_email = models.CharField(max_length=55, verbose_name="Recipient_email")
    reference = models.CharField(max_length=55, verbose_name="Extra description")

    manupulated_amount = models.DecimalField(verbose_name="Computed amount after custom FEE applied",max_digits=10, decimal_places=4, null=True, blank=True, help_text="Will be computed automatically, but can be changed afterwards.")
    
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("transferred", "Transferred"),
        ("canceled", "Canceled"),

    ], verbose_name="Status")
    

    created = models.DateTimeField(auto_now_add=True, verbose_name="Create Date")

    def __str__(self) :
        return "Request " + str(self.id) + " : " + str(self.amount) +"-"+  self.currency  


class DepositRequest(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    currency = models.CharField(max_length=255, verbose_name="Currency")
    amount = models.DecimalField(verbose_name="Amount in usd",max_digits=10,decimal_places=4, null=True, blank=True)
    url = models.CharField(max_length=255, verbose_name="payment_link")
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    order_id = models.IntegerField(verbose_name="order_id", blank=True)
    manupulated_amount = models.DecimalField(verbose_name="Computed amount after custom FEE applied",max_digits=10, decimal_places=4, null=True, blank=True, help_text="Will be computed automatically, but can be changed afterwards.")
    
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("transferred", "Transferred"),
        ("canceled", "Canceled"),

    ], verbose_name="Status")
    

    created = models.DateTimeField(auto_now_add=True, verbose_name="Create Date")

    def __str__(self) :
        return "Deposit " + str(self.id) + " : " + str(self.amount) +"-"+  self.currency  