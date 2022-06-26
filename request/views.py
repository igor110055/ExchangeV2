
from random import randint
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication 
from rest_framework.response import Response
# from .serializers import CurrencySerializer
from config.models import WebsiteConfiguration

import json
import requests

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
    _type = request.data.get("type", "bitcoin")
    amount = request.data.get("amount", 1)

    api_name = CONFIG.api_name
    secret   = CONFIG.secret_key
    password = CONFIG.password_md5


    data = {
        "name": api_name,
        "secret_key": secret,
        "password": (password).upper(),
        "type": _type,
        "amount": amount,
        "order_id": str(randint(0,10**9)),
        "description": "Payment for t-shirt ALFAcoins size XXL",
        "options": {
            "notificationURL": "http://localhost:3000/success_notification",
            "redirectURL": "http://localhost:3000/success",
            "payerName": request.user.username,
            "payerEmail": request.user.email,
        }
    }
    print(data)
    dep = DepositRequest.objects.create(user=request.user, currency=_type, amount=amount, order_id=data["order_id"], description=data["description"])
    res = requests.post("https://www.alfacoins.com/api/create.json", data=json.dumps(data), headers={
        "Content-Type" : "application/json"
    })
    try:
        result=res.json()
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
    FEE_TABLE = {
        "bitcoin": 0.0000666,
        "ethereum": 0.00102431,
        "xrp": 0.1,
        "bitcoincash": 0.000003,
        "litecoin": 0.0000678,
        "dash": 0.0000789
    }
    try:
        conf = WebsiteConfiguration.objects.get()

        _type = request.data.get("type", "bitcoin")
        amount = request.data.get("amount", 1)
        test = request.data.get("test", True)
        address = request.data.get("address", "")

        if not address: 
            return Response({
                "error": 1,
                "message" : "address is mandatory"
            })
        data = {
            "currency": _type,
            "memo": "12345678",
            "amount": amount,
            "address":address ,
            "recipient_name": "abbasebadian",
            "recipient_email": "abbasebadiann@gmail.com",
            "reference": "Caitex" + str(amount) + " Withdraw" 
        }
        calc = int(amount) - FEE_TABLE[_type] - (int(amount) * int(conf.fee) / 100)
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