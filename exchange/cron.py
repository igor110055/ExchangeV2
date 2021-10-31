from exchange.views import currency
from exchange.models import Price , Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages, Mainwalls , Forgetrequest
from django.core.management.base import BaseCommand, CommandError
import requests
import datetime as DT
import json
from exchange.models import Indexprice
import time
from time import sleep

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

def INDEXINFO():
    end = DT.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") 
    start = (DT.datetime.now() - DT.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ") 
    print(end)
    print(start)
    r = requests.get(f'https://api.nomics.com/v1/currencies/sparkline?key=5f176269caf5ea0dfab684904f9316bf1f4f2bc6&ids=BTC,ETH,TRX,DOGE,USDT&start={start}&end={end}')

    sleep(2)

    response = requests.get('https://api.nomics.com/v1/currencies/ticker?key=5f176269caf5ea0dfab684904f9316bf1f4f2bc6&ids=BTC,ETH,TRX,DOGE,USDT')

    ind = Indexprice(PriceHistory=r, price = response)
    ind.save()