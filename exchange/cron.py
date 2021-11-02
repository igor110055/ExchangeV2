from exchange.models import Indexprice, Price , Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
from django.core.management.base import BaseCommand, CommandError
import requests
import datetime as DT
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
    price.save()

def INDEXINFO():
    end = DT.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") 
    start = (DT.datetime.now() - DT.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ") 
    print(end)
    print(start)
    r = requests.get(f'https://api.nomics.com/v1/currencies/sparkline?key=5f176269caf5ea0dfab684904f9316bf1f4f2bc6&ids=BTC,ETH,TRX,DOGE,USDT&start={start}&end={end}')

    sleep(2)

    response = requests.get('https://api.nomics.com/v1/currencies/ticker?key=5f176269caf5ea0dfab684904f9316bf1f4f2bc6&ids=BTC,ETH,TRX,DOGE,USDT')
    for item in Indexprice.objects.all():
        item.delete()
    ind = Indexprice(PriceHistory=r, price = response)
    ind.save()

def RIALTICKER():
        rial = requests.get(url = 'http://api.navasan.tech/latest/?api_key=7RPe7l7pwChjXtZ3vm3xM7vl0xrOoZgk')   
        r = rial.json()
        price = Price.objects.get(id = 1)
        price.rial = int(r['usd_buy']['value']) * 10
        price.usd = int(r['usd_buy']['value']) * 10
        price.save()