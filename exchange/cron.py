from exchange.views import currency
from exchange.models import Price , Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages, Mainwalls , Forgetrequest
from django.core.management.base import BaseCommand, CommandError
import requests
import time

def TICKER():
    r = requests.get(url = 'https://api.nomics.com/v1/currencies/ticker?key=5f176269caf5ea0dfab684904f9316bf1f4f2bc6&ids=BTC,ETH,TRX,DOGE,USDT')
    r = r.json()
    price = Price.objects.get(id = 1)
    price.btc = r[0]['price']
    price.eth = r[1]['price']
    price.usdt = r[2]['price']
    price.doge = r[3]['price']
    price.trx = r[4]['price']
    price.usd = 250000
    price.save()