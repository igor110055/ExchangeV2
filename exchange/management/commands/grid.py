from exchange.models import GridBot, Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.points = 0
        def main(self):
            dbupdate()

        def dbupdate():
            allbot = GridBot.objects.all()
            self.points = []
            for i in allbot:
                gridamount = (i.upperlimit - i.lowerlimit) / i.gridsnumber
                aaa = [i.id]
                for ii in range(i.gridsnumber-1):
                    aaa.append(i.lowerlimit + (ii * gridamount))
                self.points.append(aaa)
            start=datetime.now()
            for item in self.points:
                    s = 's'
            print (datetime.now()-start)

        def slicer():
            pass

        main(self)
        print(self.points)