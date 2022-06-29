from email import header
from locale import currency
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from config.models import WebsiteConfiguration
import requests, json
from exchange.models import Currencies, Wallet
User = get_user_model()
# Create your models here.

class WithdrawRequest(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE, verbose_name="Currency")
    amount = models.FloatField(verbose_name="Amount in usd",null=True, blank=True)
    coin_amount = models.FloatField(verbose_name="Amount in currency", null=True, blank=True)
    address = models.CharField(max_length=60, verbose_name="Deposit address")
    memo = models.CharField(max_length=60, verbose_name="Address MEMO", blank=True)
    recipient_name = models.CharField(max_length=55, verbose_name="Recipient name")
    recipient_email = models.CharField(max_length=55, verbose_name="Recipient_email")
    reference = models.CharField(max_length=55, verbose_name="Extra description")
    tx_id  = models.UUIDField(verbose_name="Transaction ID", default=uuid.uuid4)
    payment_id  = models.UUIDField(verbose_name="Payment ID", default=uuid.uuid4)

    manupulated_amount = models.FloatField(verbose_name="Computed amount after custom FEE applied", null=True, blank=True, help_text="Will be computed automatically, but can be changed afterwards.")
    
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("transferred", "Transferred"),
        ("canceled", "Canceled"),

    ], verbose_name="Status", default="pending")
    

    created = models.DateTimeField(auto_now_add=True, verbose_name="Create Date")

    def __str__(self) :
        return "Request " + str(self.id) + " : " + str(self.amount) +"-"+  self.currency.name

    def confirm(self, request):
        CONFIG = WebsiteConfiguration.objects.get()
        api_name = CONFIG.api_name
        secret   = CONFIG.secret_key
        password = CONFIG.password_md5
        data = {
            "name": api_name,
            "secret_key": secret,
            "password":password,
            "type": self.currency.alfaname,
            "address": self.address,
            "memo": self.memo,
            "coin_amount": self.manupulated_amount,
            "recipient_name": "Caitex User",
            "recipient_email": self.user.email,
            "reference": "Withrawal " + str(self.manupulated_amount) + " " + self.currency.name
        }
        print(data)
        res = requests.post("https://www.alfacoins.com/api/payout.json", json.dumps(data), headers={
            "Content-Type": "application/json"
        })
        res = res.json()
        print(res)
        res = {"id": "123"}
        if type(res) == type({}) and "error" in res.keys():
            return res["error"]

        if type(res) == type({}) and "id" in res.keys():
            wall = self.user.wallet_set.filter(currency=self.currency)
            
            if not wall:
                return "No such a wallet"
            wall = wall[0]
            print( res["id"])
            wall.amount -= self.amount
            self.status = "transferred"
            wall.save()
            self.save()

            return "Payout Done! Tx_id: " + res["id"]
        
        

        return "SUCCESS"

class DepositRequest(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    currency = models.ForeignKey(Currencies, verbose_name="Currency", on_delete=models.CASCADE)
    amount = models.FloatField(verbose_name="Amount in usd", null=True, blank=True)
    url = models.CharField(max_length=255, verbose_name="payment_link")
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    manupulated_amount = models.FloatField(verbose_name="Computed amount after custom FEE applied", null=True, blank=True, help_text="Will be computed automatically, but can be changed afterwards.")
    tx_id  = models.UUIDField(verbose_name="Transaction ID", default=uuid.uuid4)
    payment_id  = models.UUIDField(verbose_name="Payment ID", default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("transferred", "Transferred"),
        ("canceled", "Canceled"),

    ], verbose_name="Status", default="pending")
    

    created = models.DateTimeField(auto_now_add=True, verbose_name="Create Date")

    def __str__(self) :
        return "Deposit " + str(self.id) + " : " + str(self.amount) +"-"+  self.currency.name