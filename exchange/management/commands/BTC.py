from exchange.views import currency
from exchange.models import Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages, Mainwalls , Forgetrequest
from django.core.management.base import BaseCommand, CommandError
import requests
import time
from bit import Key

class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in Wallet.objects.filter(currency = Currencies.objects.get(id = 2)):
            r = requests.get(url = 'https://blockchain.info/balance?active=' + item.address)
            data = r.json()
            if data[item.address]['final_balance'] > 0 :
                wall = Key(item.key)
                balance = wall.get_balance('usd')
                tx_hash = wall.send([('mkH41dfD4S8DEoSfcVSvEfpyZ9siogWWtr', balance, 'usd')])
                item.amount += balance
                item.save()
                print(tx_hash)