from exchange.models import Perpetual, PerpetualRequest, Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
import requests
from bit import Key
from django.core.management.base import BaseCommand, CommandError
from cryptos import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in Verify.objects.all():
            if len(PerpetualRequest.objects.filter(user= item.user)) < 1:
                pe = PerpetualRequest(user = item.user)
                pe.save()
            if len(Perpetual.objects.filter(user=item.user)) > 0:
                for item in PerpetualRequest.objects.filter(user= item.user):
                    item.delete()