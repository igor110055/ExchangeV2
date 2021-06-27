from exchange.views import currency
from exchange.models import Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages, Mainwalls , Forgetrequest
from django.core.management.base import BaseCommand, CommandError
from web3 import Web3
from web3.auto.infura import w3

class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in Wallet.objects.filter(currency = Currencies.objects.get(id = 3)):
            balance = w3.eth.get_balance(item.address) / 1000000000000000000
            if balance > 0 :
                signed_txn = w3.eth.account.signTransaction(dict(
                nonce=w3.eth.getTransactionCount(item.address),
                gasPrice = w3.eth.gasPrice, 
                gas = 90000,
                to='0xD02718154f4eF7c1564DEC2D519441163df08de1',
                value=int(Web3.toWei(balance,'ether'))
                ),
                item.key)
                print(w3.eth.sendRawTransaction(signed_txn.rawTransaction))