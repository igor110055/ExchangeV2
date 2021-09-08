from exchange.views import currency
from exchange.models import Leverage, Price , Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages, Mainwalls , Forgetrequest
from django.core.management.base import BaseCommand, CommandError
import requests
import time
from .lib.coinex import CoinEx

class Command(BaseCommand):
    def handle(self, *args, **options):
        Lev = Leverage.objects.all()
        for item in Lev:
                coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
                item.leverage = (coinex.margin_account(access_id='56255CA42286443EB7D3F6DB44633C25',market =  item.symbol,tonce=time.time()*1000,)['leverage'])
                item.save()