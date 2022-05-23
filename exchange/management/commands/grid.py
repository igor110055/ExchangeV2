from exchange.models import Grid, Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest, Perpetual
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
import time
import threading
import websockets
import json
import asyncio
from .lib.coinex import CoinEx

SOCKET = 'wss://socket.coinex.com/'

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.bot = {}
        def main(self):
            x = threading.Thread(target=dbupdate)
            x.start()
#            y = threading.Thread(target=observer)
#           y.start()
            
            asyncio.run(observer())

        def dbupdate():
            allbot = Grid.objects.all()
            self.bot = {}
            for i in allbot:
                print(Grid.objects.values())
                aaa = {}
                aaa['points'] = []
                gridamount = (i.upper - i.lower) / i.grid
                per = Perpetual.objects.get(user = i.user)
                aaa['access_id'] = per.apikey
                aaa['secret_key'] = per.secretkey
                aaa['stepamount'] = i.total / i.grid
                coinex = CoinEx(per.apikey, per.secretkey )
                aaa['accountid'] = coinex.margin_account(market =  i.market)['account_id']
                for ii in range(i.grid-1):
                    aaa['points'].append(i.lower + (ii * gridamount))
                self.bot[i.market] = aaa
            start=datetime.now()
            print (datetime.now()-start)
            print(self.bot)
            time.sleep(60)
            dbupdate()
        
        def on_open(ws):
            print('o')
        def on_close(ws):
            print('c')
        def on_message(ws , message):
            print('message')

        async def observer():

            async with websockets.connect(SOCKET) as websocket:
                name = 'n'
                param = {
                    "id": 1,
                    "method": "state.query",
                    "params": [
                        "SOLUSDT",
                        86400
                    ]
                }

                while True:
                    await websocket.send(json.dumps(param))
                    greeting = await websocket.recv()
                    print(f"<<< {json.loads(greeting)['result']['last']}")
                    time.sleep(2)
                    
        main(self)