
from random import randint
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication , SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework import authentication
from exchange.models import Currencies, Wallet
# from .serializers import CurrencySerializer
from config.models import WebsiteConfiguration

import json
import requests
from django.shortcuts import render
from .models import DepositRequest, WithdrawRequest

@api_view(['GET', 'POST'])
def pair_price(request):
    try:
        pair = request.data.get("pair", "__")
        res = requests.get(f"https://www.alfacoins.com/api/rate/{pair}.json")
        result=res.json()
        if type(result) == type([]):
            return Response({
                "error": 0,
                "message": "Redirecting...",
                "price": result[0]
            })
        raise Exception(result.get("error", "error"))
    except Exception as e:
        return Response({
            "error": 1,
            "message": "Some error occured",
            "extra": str(e)
        })


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def deposit(request):
    CONFIG = WebsiteConfiguration.objects.get()
    api_name = CONFIG.api_name
    secret   = CONFIG.secret_key
    password = CONFIG.password_md5
    _type = request.data.get("type", "bitcoin")
    amount = request.data.get("amount", 1)


    currency = Currencies.objects.filter(alfaname=_type)
    if not currency:
        return Response({
            "error": 1,
            "message": "Invalid Currency"
        })
    dep = DepositRequest.objects.create(user=request.user, currency=currency.first(), amount=amount, description="Deposit " + str(amount) + " USD")

    data = {
        "name": api_name,
        "secret_key": secret,
        "password": (password).upper(),
        "type": _type,
        "amount": amount,
        "order_id": str(dep.tx_id),
        "description": "Deposit " + str(amount) + " USD",
        "options": {
            "notificationURL": "http://localhost:3000/success_notification",
            "redirectURL": "http://localhost:8000/payments/result/" + str(dep.payment_id),
            "payerName": request.user.username,
            "payerEmail": request.user.email
        }
    }
    for k,v in data.items():
        
        if k == "options":
            print("options:")
            for y,z in v.items():
                print("\t",y," : " ,z)
        else:
            if k == "password":
                v = "A String Passowrd :D" 
            print(k," : " ,v)

        
    
    res = requests.post("https://www.alfacoins.com/api/create.json", data=json.dumps(data), headers={
        "Content-Type" : "application/json"
    })
    try:
        result=res.json()
        for k,v in result.items():
            print(k, " : ", v)
        dep.manupulated_amount = result['coin_amount']
        if result.get("url", None):
            dep.url = result.get("url", "")
            dep.save()
            return Response({
                "error": 0,
                "message": "Redirecting...",
                "url": result.get("url", "")
            })
        dep.delete()
        raise Exception(result.get("error", "error"))
    except Exception as e:
        return Response({
            "error": 1,
            "message": "Some error occured",
            "extra": str(e)
        })


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])

def withdraw(request):
    try:
        _type = request.data.get("type", "bitcoin")
        res = requests.get("https://www.alfacoins.com/api/fees.json")
        res = res.json()
        FEE1 = res[_type]["payout"]["network_fee"].split()[0]
        FEE2 = res[_type]["payout"]["commission"].replace("%", '').strip()
        conf = WebsiteConfiguration.objects.get()

        amount = float(request.data.get("amount", 0))
        address = request.data.get("address", "")
        currency = Currencies.objects.filter(alfaname=_type)
        if not currency:
            return Response({
                "error": 1,
                "message": "Invalid Currency"
            })
        if not address: 
            return Response({
                "error": 1,
                "message" : "address is mandatory"
            })
        data = {
            "currency": currency[0],
            "memo": "12345678",
            "coin_amount": amount,
            "address":address ,
            "recipient_name": request.user.username,
            "recipient_email": request.user.email,
            "reference": "Caitex" + str(amount) + " Withdraw" 
        }
        calc = float(amount) - (float(amount) * (float(conf.fee) + float(FEE2)) / 100) - float(FEE1)
        wall = Wallet.objects.filter(user=request.user, currency=currency[0])
        if not wall or wall[0].amount < calc:
            return Response({
                "error": 1,
                "message" : "Not enough balance"
            })
        c = WithdrawRequest.objects.create(**data, status="pending", user=request.user, manupulated_amount=calc)
        return Response({
            "error": 0,
            "message": "Successfully Created",
            "id": c.id
        })
    except Exception as e:
        return Response({
            "error": 1,
            "message": "Some Error ocurred",
            "extra": str(e)
        })


@api_view(['GET'])
@authentication_classes([ TokenAuthentication])
def handle_success(request, payment_id):
    data = {
        "header": "",
        "text": "",
        "type": "error"
    }
    dep = DepositRequest.objects.filter(payment_id=payment_id)
    if not dep:
        data["header"] = "Payment ID invalid."
        return Response( data )
    dep = dep.first()
    if dep.status != "pending":
        data["header"] = "Payment Already handled"
        return Response( data )

    data["header"] = "Payment Successful"
    data["text"] = dep.description
    dep.status = "transferred"
    wallet, c = Wallet.objects.get_or_create(user=request.user,currency=dep.currency)
    wallet.amount += float(dep.manupulated_amount)  
    wallet.save()
    dep.save()
    return Response( data )


@api_view(['GET'])
def commision(request):
    CONFIG = WebsiteConfiguration.objects.get()
    fee = CONFIG.fee

    res = requests.get("https://www.alfacoins.com/api/fees.json")
    res = res.json()
    nres = {}
    for k,v in res.items(): #bit, eth
        v["withdrawal"]["commission"] = str(float(v["payout"]["commission"].replace("%", "").strip())+ float(fee)) + "%" 
        v["withdrawal"]["network_fee"] = v["payout"]["network_fee"]
        nres[k] = v

    return Response( nres )