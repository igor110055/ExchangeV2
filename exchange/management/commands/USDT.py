from exchange.views import currency
from exchange.models import Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages, Mainwalls , Forgetrequest
from django.core.management.base import BaseCommand, CommandError
import requests
import time
from bit import Key
import json
import logging
import requests
import base58
import base64
from pprint import pprint


from tronapi import Tron
full_node = 'https://api.trongrid.io'
solidity_node = 'https://api.trongrid.io'
event_server = 'https://api.trongrid.io/'

tron = Tron(full_node=full_node,
            solidity_node=solidity_node,
            event_server=event_server)

class Command(BaseCommand):
    def address_to_parameter(addr):
        return "0" * 24 + base58.b58decode_check(addr)[1:].hex()

    url = 'https://api.trongrid.io/' + 'wallet/triggerconstantcontract'
    payload = {
        'owner_address': base58.b58decode_check("4177ec41598752f09176f3099a034a49054828fdf1").hex(),
        'contract_address': base58.b58decode_check('TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t').hex(),
        'function_selector':'balanceOf(address)',
        'parameter': address_to_parameter('4177ec41598752f09176f3099a034a49054828fdf1'),
    }
    resp = requests.post(url, json=payload)
    data = resp.json()

    if data['result'].get('result', None):
        print(data['constant_result'])
        val = data['constant_result'][0]
        print('balance =', int(val, 16))
    else:
        print('error:', bytes.fromhex(data['result']['message']).decode())

            