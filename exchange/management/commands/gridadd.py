from exchange.models import GridBot, Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in range(1 , 4999):
            gg = GridBot.objects.get(id = item)
            gg.gridsnumber = 100
            gg.save()