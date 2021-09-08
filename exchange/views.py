from requests.sessions import Request
from exchange.lib import request_client
from typing import Text
from django import http
from django.http import response
import requests
from .lib.request_client import RequestClient
from .lib.coinex import CoinEx
from bitmerchant.wallet import Wallet as Wall
import time
from django.db.models.fields import EmailField
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from rest_framework import request, serializers
from django.http import HttpResponse , Http404 
from rest_framework import status
from rest_framework import authentication
from .serializers import LeverageSerializer, ProTradesBuyOrderSerializer, ProTradesSellOrderSerializer , MainTradesBuyOrderSerializer, MainTradesSellOrderSerializer, ProTradesSerializer, MainTradesSerializer, NotificationSerializer, BankAccountsSerializer, VerifyBankAccountsRequest , PriceSerializer , StaffSerializer, UserInfoSerializer, VerifyBankAccountsRequestSerializer, VerifyMelliRequestSerializer , WalletSerializer , CurrenciesSerializer ,VerifySerializer, BankCardsSerializer, TransactionsSerializer, SettingsSerializer, SubjectsSerializer, TicketsSerializer, PagesSerializer , UserSerializer , ForgetSerializer, VerifyBankRequestSerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from .models import Leverage, PriceHistory, mobilecodes, ProTradesSellOrder, MainTradesSellOrder,ProTradesBuyOrder, MainTradesBuyOrder, ProTrades, MainTrades, Notification , VerifyBankAccountsRequest , BankAccounts, Price, Staff,  UserInfo , Currencies, VerifyMelliRequest , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages, Mainwalls , Forgetrequest , VerifyBankRequest
from django.contrib.auth.models import AbstractUser , User
from django.contrib.auth.decorators import user_passes_test
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from py_crypto_hd_wallet import HdWalletFactory, HdWalletCoins, HdWalletSpecs , HdWalletWordsNum, HdWalletChanges
import json
from datetime import datetime ,timedelta
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from ippanel import Client
import pytz
from random import randrange
import requests
from itertools import chain
from eth_account import Account
import secrets
import logging
import copy
import hashlib
import time
import traceback
from .lib import CoinexPerpetualApi
from django.db.models import Q

class bsc(APIView):

    def get(self , request , format=None):

        hd_wallet_fact = HdWalletFactory(HdWalletCoins.BINANCE_SMART_CHAIN)
        hd_wallet = hd_wallet_fact.CreateRandom("my_wallet_name", HdWalletWordsNum.WORDS_NUM_12)
        hd_wallet.Generate(account_idx = 1, change_idx = HdWalletChanges.CHAIN_EXT, addr_num = 1)
        wallet_data = hd_wallet.ToJson()
        return Response(wallet_data)


class usersinfo(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get_object(self , user):
        try:
            return UserInfo.objects.filter(user = user)
        except UserInfo.DoesNotExist:
            return Http404

    def get(self , request , format=None):
        if len(Notification.objects.filter(user = request.user)) < 1 : 
            note = Notification(user = request.user , title = 'خوش آمدید' , text = 'به AMIZAX خوش آمدید') 
            note.save()
        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(request.user)
        serializer = UserInfoSerializer(userinfo , many=True)
        return Response(serializer.data)
    
    def post(self, request , format=None):
        if len(UserInfo.objects.filter(user = request.user)) < 1:
            u = UserInfo(user = request.user, first_name = request.data['first_name'], last_name = request.data['last_name'], mobile = request.data['mobile'], email = request.data['email'])
            u.save()
            note = Notification(user = request.user , title = ' اطلاعات شما با موفقیت ثبت شد' , text = 'برای شروع معاملات لطفا احراز هویت را انجام دهید') 
            note.save()
            return Response( status=status.HTTP_201_CREATED)
        else:
            user = UserInfo.objects.get(user = request.user)
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.mobile = request.data['mobile']
            user.email = request.data['email']
            user.save()
            return Response( status=status.HTTP_201_CREATED)



class dashboardinfo(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        item = User.objects.get(id= request.user.id)
        if len(UserInfo.objects.filter(user = item)) > 0:
                userinfos = UserInfo.objects.get(user = item)
                wallet= 0
                wallets= []
                price = 0
                users=[]
                userinfos = UserInfo.objects.get(user = request.user)
                openorder = len(MainTradesBuyOrder.objects.filter(user = request.user)) + len(MainTradesSellOrder.objects.filter(user = request.user)) + len(ProTradesBuyOrder.objects.filter(user = request.user)) + len(ProTradesSellOrder.objects.filter(user = request.user))
                opens = list(chain(MainTradesBuyOrder.objects.filter(user = request.user), MainTradesSellOrder.objects.filter(user = request.user), ProTradesBuyOrder.objects.filter(user = request.user), ProTradesSellOrder.objects.filter(user = request.user)))
                openorders = MainTradesSellOrderSerializer(opens , many=True).data
                unread = 0 
                for items in Subjects.objects.filter(user = request.user):
                    if not items.read :
                        unread = unread + 1
                for itemm in Wallet.objects.filter(user = request.user):
                    if itemm.currency.id == 1:
                        price = 1
                    elif itemm.currency.id == 2:
                        price = Price.objects.get(id = 1).btc * Price.objects.get(id = 1).usd
                    elif itemm.currency.id == 3:
                        price = Price.objects.get(id = 1).eth * Price.objects.get(id = 1).usd
                    elif itemm.currency.id == 4:
                        price = Price.objects.get(id = 1).usdt * Price.objects.get(id = 1).usd
                    elif itemm.currency.id == 5:
                        price = Price.objects.get(id = 1).trx * Price.objects.get(id = 1).usd
                    elif itemm.currency.id == 6:
                        price = Price.objects.get(id = 1).doge * Price.objects.get(id = 1).usd
                    wallet = wallet + (itemm.amount * price)
                    wallets.append({'brand': itemm.currency.brand, 'amount': itemm.amount * price})
                users.append({'username': item.username, 'level': userinfos.level, 'balance': wallet, 'is_active': userinfos.is_active, 'is_admin': userinfos.is_admin, 'id': item.id, 'openorder': openorder, 'unread': unread, 'openorders': openorders, 'wallets': wallets})
        return Response(users)

class user(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def get_object(self , user):
        try:
            return User.objects.filter(id = user.id)
        except UserInfo.DoesNotExist:
            return Http404

    def get(self , request , format=None):
        userinfo =  self.get_object(request.user)
        serializer = UserSerializer(userinfo , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        userinfo =  User.objects.all()
        serializer = UserSerializer(userinfo , many=True)
        return Response(serializer.data)

class wallets(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get_object(self , user):
        try:
            return Wallet.objects.filter(user = user)
        except Wallet.DoesNotExist:
            return Http404
            
    def get(self , request , format=None):
        userinfo = self.get_object(request.user.id)
        serializer = WalletSerializer(userinfo , many=True)
        return Response(serializer.data)

class price(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
            
    def get(self , request , format=None):
        price = Price.objects.filter(id=1)
        serializer = PriceSerializer(price , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

class leverages(APIView):
            
    def get(self , request , format=None):
        price = Leverage.objects.all()
        list={}
        for item in price :
            list[f'{item.symbol}'] = item.leverage
        return Response(list , status=status.HTTP_201_CREATED)



class pricehistory(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
            
    def get(self , request , format=None):
        pricehis = {'rial': [],'btc': [],'eth': [],'trx': [],'usdt': [],'doge': [],'usd': [], }
        price = PriceHistory.objects.all().order_by('-id')[:7]
        for item in price:
            pricehis['rial'].append(item.rial)
            pricehis['btc'].append(item.btc)
            pricehis['eth'].append(item.eth)
            pricehis['trx'].append(item.trx)
            pricehis['usdt'].append(item.usdt)
            pricehis['doge'].append(item.doge)
            pricehis['usd'].append(item.usd)
        return Response(pricehis , status=status.HTTP_201_CREATED)

class wallet(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get_object(self , user , id):
        try:
            return Wallet.objects.filter(user = user , currency = id)
        except Wallet.DoesNotExist:
            return Http404
            
    def get(self , request , id):
        userinfo = self.get_object(request.user.id , id)
        serializer = WalletSerializer(userinfo , many=True)
        return Response(serializer.data)

    def post(self ,request , id):
        if id == 5 :
            url = "https://api.shasta.trongrid.io/wallet/generateaddress"
            headers = {"Accept": "application/json"}
            response = requests.request("GET", url, headers=headers)
            print(response.json()['hexAddress'])
            address = response.json()['hexAddress']
            key = response.json()['privateKey']
            if len(Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = id))) > 0:
                wa = Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = id))
                wa.key = key
                wa.address = address
                wa.save()
            else:
                wa = Wallet(user = request.user , currency = Currencies.objects.get(id = id) , amount = 0 , address = address , key = key)
                wa.save()
            return Response(status=status.HTTP_201_CREATED)
        if id == 2 :
            my_wallet = Wall.new_random_wallet() 
            key = my_wallet.serialize()
            address = my_wallet.to_address()
            if len(Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = id))) > 0:
                wa = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = id))
                wa.key = key
                wa.address = address
                wa.save()
            else:
                wa = Wallet(user = request.user , currency = Currencies.objects.get(id = id) , amount = 0 , address = address , key = key)
                wa.save()
            return Response(status=status.HTTP_201_CREATED)

        if id == 3 :
            priv = secrets.token_hex(32)
            private_key = "0x" + priv
            acct = Account.from_key(private_key)
            address = acct.address
            key = private_key
            if len(Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = id))) > 0:
                wa = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = id))
                wa.key = key
                wa.address = address
                wa.save()
            else:
                wa = Wallet(user = request.user , currency = Currencies.objects.get(id = id) , amount = 0 , address = address , key = key)
                wa.save()
            return Response(status=status.HTTP_201_CREATED)
        if id == 6 :
            seed = Wal.generate_mnemonic()
            w = Wal.create_wallet(network="DOGE", seed=seed, children=1)
            address = w['address']
            key = w['wif']
            if len(Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = id))) > 0:
                wa = Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = id))
                wa.key = key
                wa.address = address
                wa.save()
            else:
                wa = Wallet(user = request.user , currency = Currencies.objects.get(id = id) , amount = 0 , address = address , key = key)
                wa.save()
            return Response(status=status.HTTP_201_CREATED)

        if id == 4 :
            if len(Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = 5))) > 0 :
                if len(Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = id))) > 0:
                    wa = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = id))
                    wa.key = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = 5)).key
                    wa.address = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = 5)).address
                    wa.save()
                else:
                    wa = Wallet(user = request.user , currency = Currencies.objects.get(id = id) , amount = 0 , address = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = 5)).address , key = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = 5)).key)
                    wa.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                url = "https://api.shasta.trongrid.io/wallet/generateaddress"
                headers = {"Accept": "application/json"}
                response = requests.request("GET", url, headers=headers)
                print(response.json()['address'])
                address = response.json()['address']
                key = response.json()['privateKey']
                if len(Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = id))) > 0:
                    wa = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = id))
                    wa.key = key
                    wa.address = address
                    wa.save()
                    wa2 = Wallet(user = request.user , currency = Currencies.objects.get(id = 5) , amount = 0 , address = address , key = key)
                    wa2.save()
                else:
                    wa = Wallet(user = request.user , currency = Currencies.objects.get(id = id) , amount = 0 , address = address , key = key)
                    wa.save()
                    wa2 = Wallet(user = request.user , currency = Currencies.objects.get(id = 5) , amount = 0 , address = address , key = key)
                    wa2.save()
                return Response(status=status.HTTP_201_CREATED)

        if id == 41 :
            id = 4
            if len(Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = 3))) > 0 :
                if len(Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = id))) > 0:
                    wa = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = id))
                    wa.key2 = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = 3)).key
                    wa.address2 = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = 3)).address
                    wa.save()
                else:
                    wa = Wallet(user = request.user , currency = Currencies.objects.get(id = id) , amount = 0 , address2 = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = 3)).address , key2 = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = 3)).key)
                    wa.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                priv = secrets.token_hex(32)
                private_key = "0x" + priv
                acct = Account.from_key(private_key)
                address = acct.address
                key = private_key
                if len(Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = id))) > 0:
                    wa = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = id))
                    wa.key2 = key
                    wa.address2 = address
                    wa.save()
                    wa2 = Wallet(user = request.user , currency = Currencies.objects.get(id = 3) , amount = 0 , address = address , key = key)
                    wa2.save()
                else:
                    wa = Wallet(user = request.user , currency = Currencies.objects.get(id = id) , amount = 0 , address2 = address , key2 = key)
                    wa.save()
                    wa2 = Wallet(user = request.user , currency = Currencies.objects.get(id = 3) , amount = 0 , address = address , key = key)
                    wa2.save()
                return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class currency(APIView):

    def get_object(self , id):
        try:
            return Currencies.objects.filter(id = id)
        except Wallet.DoesNotExist:
            return Http404
            
    def get(self , request ,id):
        userinfo = self.get_object(id)
        serializer = CurrenciesSerializer(userinfo , many=True)
        return Response(serializer.data)

class currencies(APIView):

    def get_object_all(self):
        try:
            return Currencies.objects.all().order_by('id')
        except Wallet.DoesNotExist:
            return Http404
            
    def get(self , request):
        userinfo = self.get_object_all()
        serializer = CurrenciesSerializer(userinfo , many=True)
        return Response(serializer.data)


class verify(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def get_object(self , user):
        if(len(Verify.objects.filter(user = user))<1):
            verif = Verify(user = user)
            verif.save()
        try:
            return Verify.objects.filter(user = user)
        except Wallet.DoesNotExist:
            return Http404
            
    def get(self , request , format=None):
        verify = self.get_object(request.user)
        serializer = VerifySerializer(verify , many=True)
        return Response(serializer.data)

class bankcards(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get_object(self , user):
        try:
            return BankCards.objects.filter(user = user)
        except Wallet.DoesNotExist:
            return Http404
            
    def get(self , request , format=None):
        bankcards = self.get_object(request.user)
        serializer = BankCardsSerializer(bankcards , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        request.data['user'] = request.user.id
        serializer = VerifyBankRequestSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class bankaccounts(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get_object(self , user):
        try:
            return BankAccounts.objects.filter(user = user)
        except BankAccounts.DoesNotExist:
            return Http404
            
    def get(self , request , format=None):
        bankaccounts = self.get_object(request.user)
        serializer = BankAccountsSerializer(bankaccounts , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        request.data['user'] = request.user.id
        serializer = VerifyBankAccountsRequestSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class transactions(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def get_object(self , user):
        try:
            return Transactions.objects.filter(user = user)
        except Wallet.DoesNotExist:
            return Http404
            
    def get(self , request , format=None):
        transactions = self.get_object(request.user)
        serializer = TransactionsSerializer(transactions , many=True)
        return Response(serializer.data)


class settings(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def get_object(self):
        try:
            return Settings.objects.filter(id = 1)
        except Wallet.DoesNotExist:
            return Http404
            
    def get(self , request , format=None):
        settings = self.get_object()
        serializer = SettingsSerializer(settings , many=True)
        return Response(serializer.data)

    def put(self , request , format=None):
        request.data['id'] = 1
        serializer = Settings.objects.get(id=1)
        serializer.data = request.data
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class pages(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def get_object(self):
        try:
            return Pages.objects.all()
        except Wallet.DoesNotExist:
            return Http404
            
    def get(self , request , format=None):
        pages = self.get_object()
        serializer = PagesSerializer(pages , many=True)
        return Response(serializer.data)

class addforget(APIView):
    def post(self , request , format=None):
        if(len(User.objects.filter(email = request.data['email']))<1):
            return Response({
            'error' : 'کاربر با ایمیل وارد شده یافت نشد'
        }, status=status.HTTP_404_NOT_FOUND)
        serializer = ForgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = request.data['email']
            key = Forgetrequest.objects.filter(email = email).reverse()[0].key
            response_data = {}
            response_data['result'] = 'Create post successful!'
            send_mail(
            'Subject here',
            f' ',
            'info@ramabit.com',
            [f'{email}'],
            fail_silently=False,
        )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class resetpass(APIView):
    def get(self , request ,key, format=None):
        utc=pytz.UTC
        
        if(Forgetrequest.objects.get(key = key).date + timedelta(minutes = 10) > utc.localize(datetime.now())):
            return redirect(f"http://localhost:8080/resetpass/{key}")
        else:
            return redirect(f"http://localhost:8080/expired")

    def post(self , request):
        key = request.data['key']
        if(len(Forgetrequest.objects.filter(key = request.data['key']))<1):
            return redirect(f"http://localhost:8080/expired")
        user = User.objects.get(email = Forgetrequest.objects.get(key = request.data['key']).email)
        passw = request.data['password']
        repassw = request.data['repassword']
        if passw == repassw:
            passs = make_password(str(passw))
            user.password = passs
            user.save()
            return redirect(f"http://localhost:8080/login")

class mobileverify(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def put(self , request):
        vcode = randrange(123456,999999)
        a = mobilecodes.objects.filter(number = request.data['number'])
        for item in a:
            item.delete()
        c = mobilecodes(number = request.data['number'], code = vcode)
        c.save()

        sms = Client("HpmWk_fgdm_OnxGYeVpNE1kmL8fTKC7Fu0cuLmeXQHM=")

        pattern_values = {
        "verification-code": f"{vcode}",
        }

        bulk_id = sms.send_pattern(
            "pifmmqr30d",    # pattern code
            "+983000505",      # originator
            f"+98{request.data['number']}",  # recipient
            pattern_values,  # pattern values
        )

        message = sms.get_message(bulk_id)
        print(message)
        print(f"+98{request.data['number']}")
        return Response(status=status.HTTP_200_OK )

    def post(self , request):
        user = Verify.objects.get(user= request.user)
        c = mobilecodes.objects.get(number= request.data['number'])
        if(int(request.data['code']) == int(c.code)):
            user.mobilev = True
            user.save()
            mobile = UserInfo.objects.get(user = request.user)
            mobile.mobile = request.data['number']
            mobile.save()
            if (user.melliv == 3 and user.mobilev == True ):
                per = User.objects.get(id = request.user.id)
                per.level = 1
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"error": "کد وارد شده معتبر نیست"} , status=status.HTTP_400_BAD_REQUEST)

class emailverify(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def put(self , request):
        user = Verify.objects.get(user= request.user)
        vcode = randrange(123456, 999999)
        user.emailc = vcode
        user.save()
        
        send_mail(
            'Subject here',
            f'به شرکت سرمایه گذاری ... خوش آمدید کد فعالسازی : {vcode} ',
            'info@ramabit.com',
            [f'{request.data["email"]}'],
            fail_silently=False,
        )
        return Response(status=status.HTTP_200_OK)

    def post(self , request):
        user = Verify.objects.get(user= request.user)
        if(int(request.data['code']) == int(user.emailc)):
            user.emailv = True
            user.save()
            mail = request.user
            mail.email = request.data['email']
            mail.save()
            if (user.melliv == 3 and user.mobilev == True ):
                per = User.objects.get(id = request.user.id)
                per.level = 1
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"error": "کد وارد شده معتبر نیست"} , status=status.HTTP_400_BAD_REQUEST)

class verifymelli(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self , request , format=None):
        request.data['user'] = request.user.id
        serializer = VerifyMelliRequestSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class bankrequests(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get_object(self , user):
        return VerifyBankRequest.objects.filter(user = user)

    def get(self , request , format=None):
        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(request.user)
        serializer = VerifyBankRequestSerializer(userinfo , many=True)
        return Response(serializer.data)

class notifications(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self , user):
        return Notification.objects.filter(user = user)

    def get(self , request , format=None):
        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(request.user)
        serializer = NotificationSerializer(userinfo , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(request.user)
        for item in userinfo :
            item.seen = True
            item.save()
            return Response(status=status.HTTP_201_CREATED)

class subject(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self , user):
        return Subjects.objects.filter(user = user)

    def get(self , request , format=None):
        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(request.user)
        serializer = SubjectsSerializer(userinfo , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        request.data['user'] = request.user.id
        sub = Subjects(user = request.user , title = request.data['title'])
        sub.save()
        request.data['subid'] = Subjects.objects.filter(user = request.user).order_by('-date')[0].id
        serializer = TicketsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self , request , format=None):
        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(request.user)
        for item in userinfo :
            item.read = True
            item.save()
            return Response(status=status.HTTP_201_CREATED)

class ticket(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self , id):
        return Tickets.objects.filter(subid = id)

    def get(self , request , id , format=None):
        if len(self.get_object(id)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(id)
        serializer = TicketsSerializer(userinfo , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        request.data['user'] = request.user.id
        serializer = TicketsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class maintrades(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return MainTrades.objects.all()

    def get(self , request , format=None):
        if len(self.get_object()) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object()
        serializer = MainTradesSerializer(userinfo , many=True)
        return Response(serializer.data)

    def post(self , request, id , format=None):
        if len(self.get_object()) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  MainTrades.objects.filter(id = id)
        serializer = MainTradesSerializer(userinfo , many=True)
        return Response(serializer.data)

class protrades(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return ProTrades.objects.all()

    def get(self , request , format=None):
        if len(self.get_object()) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object()
        serializer = ProTradesSerializer(userinfo , many=True)
        return Response(serializer.data)

    def post(self , request, id , format=None):
        if len(self.get_object()) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  ProTrades.objects.filter(id = id)
        serializer = ProTradesSerializer(userinfo , many=True)
        return Response(serializer.data)

class fasttorial(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get(self , request , id , format=None):
        uprice = price = Price.objects.get(id = 1).usd
        if (Currencies.objects.get(id = id).brand == 'BTC'):
            price = Price.objects.get(id = 1).btc
        if (Currencies.objects.get(id = id).brand == 'ETH'):
            price = Price.objects.get(id = 1).eth
        if (Currencies.objects.get(id = id).brand == 'USDT'):
            price = Price.objects.get(id = 1).usdt
        if (Currencies.objects.get(id = id).brand == 'TRX'):
            price = Price.objects.get(id = 1).trx
        if (Currencies.objects.get(id = id).brand == 'DOGE'):
            price = Price.objects.get(id = 1).doge
        wallet = Wallet.objects.get(user=request.user , currency = Currencies.objects.get(id = id))
        amount = wallet.amount
        return Response({'price': price*amount*uprice} , status=status.HTTP_201_CREATED)

    def post(self , request , id , format=None):
        uprice = price = Price.objects.get(id = 1).usd
        if (Currencies.objects.get(id = id).brand == 'BTC'):
            price = Price.objects.get(id = 1).btc
        if (Currencies.objects.get(id = id).brand == 'ETH'):
            price = Price.objects.get(id = 1).eth
        if (Currencies.objects.get(id = id).brand == 'USDT'):
            price = Price.objects.get(id = 1).usdt
        if (Currencies.objects.get(id = id).brand == 'TRX'):
            price = Price.objects.get(id = 1).trx
        if (Currencies.objects.get(id = id).brand == 'DOGE'):
            price = Price.objects.get(id = 1).doge
        wallet = Wallet.objects.get(user=request.user , currency = Currencies.objects.get(id = id))
        amount = wallet.amount
        ramount = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = 1))
        ramount.amount += price*amount*uprice
        ramount.save()
        wallet.amount = 0
        wallet.save()
        return Response(status=status.HTTP_201_CREATED)

class maintradebuyorders(APIView):

    def get_object(self , id):
        return MainTradesBuyOrder.objects.filter(trade = MainTrades.objects.get(id = id))

    def get(self, request, id, format=None):
        if len(self.get_object(id)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(id)
        serializer = MainTradesBuyOrderSerializer(userinfo , many=True)
        return Response(serializer.data)
    
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def post(self , request ,id , format=None):
        amount = float(request.data['amount'])
        amountstart = float(request.data['amount'])
        price = float(request.data['price'])
        trade = id
        user = request.user
        sells = MainTradesSellOrder.objects.filter(price__lte = request.data['price'] , trade = MainTrades.objects.get(id = id)).order_by('-price')
        i=0
        if amount * price > Wallet.objects.get(user = request.user , currency = MainTrades.objects.get(id = trade).scurrency).amount :
            return Response({
            'error' : "موجودی کافی نیست"
        }, status=status.HTTP_400_BAD_REQUEST)
        if len(sells) > 0 :
            while i < len(sells) or amount == 0:
                item = sells[i]
                if amount < item.amount :
                    wal = Wallet.objects.get(user = item.user , currency = MainTrades.objects.get(id = trade).scurrency)
                    wal.amount = wal.amount + (amount * item.price)
                    wal.save()
                    wal2 = Wallet.objects.get(user = request.user , currency = MainTrades.objects.get(id = trade).scurrency)
                    wal2.amount = wal.amount - (amount * item.price)
                    wal2.save()
                    wal3 = Wallet.objects.get(user = request.user , currency = MainTrades.objects.get(id = trade).bcurrency)
                    wal3.amount = wal.amount + amount
                    wal3.save()
                    amount = item.amount - amount
                    item.save()
                    amount = 0

                elif amount == item.amount :
                    wal = Wallet.objects.get(user = item.user , currency = MainTrades.objects.get(id = trade).scurrency)
                    wal.amount = wal.amount + (amount * item.price)
                    wal.save()
                    wal2 = Wallet.objects.get(user = request.user , currency = MainTrades.objects.get(id = trade).scurrency)
                    wal2.amount = wal.amount - (amount * item.price)
                    wal2.save()
                    wal3 = Wallet.objects.get(user = request.user , currency = MainTrades.objects.get(id = trade).bcurrency)
                    wal3.amount = wal.amount + amount
                    wal3.save()
                    item.delete()
                    amount = 0

                else :

                    wal = Wallet.objects.get(user = item.user , currency = MainTrades.objects.get(id = trade).scurrency)
                    wal.amount = wal.amount + (amount * item.price)
                    wal.save()
                    wal2 = Wallet.objects.get(user = request.user , currency = MainTrades.objects.get(id = trade).scurrency)
                    wal2.amount = wal.amount - (amount * item.price)
                    wal2.save()
                    wal3 = Wallet.objects.get(user = request.user , currency = MainTrades.objects.get(id = trade).bcurrency)
                    wal3.amount = wal.amount + amount
                    wal3.save()
                    amount = amount - item.amount
                    item.delete()
                    i = i +1
            if amount > 0 :
                add = MainTradesBuyOrder(trade = MainTrades.objects.get(id = trade) ,user = request.user, amount = amount , price = price , start = amountstart)
                add.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_201_CREATED)
        else:
            add = MainTradesBuyOrder(trade = MainTrades.objects.get(id = trade) ,user = request.user, amount = amount , price = price, start = amountstart)
            add.save()
            return Response(status=status.HTTP_201_CREATED)
    

class maintradesellorders(APIView):

    def get_object(self , id):
        return MainTradesSellOrder.objects.filter(trade = MainTrades.objects.get(id = id))

    def get(self, request, id, format=None):
        if len(self.get_object(id)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(id)
        serializer = MainTradesSellOrderSerializer(userinfo , many=True)
        return Response(serializer.data)
    
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def post(self , request, id , format=None):
        amount = float(request.data['amount'])
        amountstart = float(request.data['amount'])
        price = float(request.data['price'])
        trade = id
        user = request.user
        buys = MainTradesBuyOrder.objects.filter(price__gte = request.data['price'], trade = MainTrades.objects.get(id = trade)).order_by('price')
        i=0
        if amount > Wallet.objects.get(user = request.user , currency = MainTrades.objects.get(id = trade).bcurrency).amount :
            return Response({
            'error' : "موجودی کافی نیست"
        }, status=status.HTTP_400_BAD_REQUEST)
        if len(buys) > 0 :
            while i < len(buys) or amount == 0:
                item = buys[i]
                if amount < item.amount :
                    wal = Wallet.objects.get(user = item.user , currency = MainTrades.objects.get(id = trade).bcurrency)
                    wal.amount = wal.amount + amount
                    wal.save()
                    wal2 = Wallet.objects.get(user = request.user , currency = MainTrades.objects.get(id = trade).scurrency)
                    wal2.amount = wal.amount + (amount * item.price)
                    wal2.save()
                    wal3 = Wallet.objects.get(user = request.user , currency = MainTrades.objects.get(id = trade).bcurrency)
                    wal3.amount = wal.amount - amount
                    wal3.save()
                    item.amount = item.amount - amount
                    item.save()
                    amount = 0

                elif amount == item.amount :
                    wal = Wallet.objects.get(user = item.user , currency = MainTrades.objects.get(id = trade).bcurrency)
                    wal.amount = wal.amount + amount
                    wal.save()
                    wal2 = Wallet.objects.get(user = request.user , currency = MainTrades.objects.get(id = trade).scurrency)
                    wal2.amount = wal.amount + (amount * item.price)
                    wal2.save()
                    wal3 = Wallet.objects.get(user = request.user , currency = MainTrades.objects.get(id = trade).bcurrency)
                    wal3.amount = wal.amount - amount
                    wal3.save()
                    item.delete()
                    amount = 0
                
                elif amount > item.amount :

                    wal = Wallet.objects.get(user = item.user , currency = MainTrades.objects.get(id = trade).bcurrency)
                    wal.amount = wal.amount + amount
                    wal.save()
                    wal2 = Wallet.objects.get(user = request.user , currency = MainTrades.objects.get(id = trade).scurrency)
                    wal2.amount = wal.amount + (amount * item.price)
                    wal2.save()
                    wal3 = Wallet.objects.get(user = request.user , currency = MainTrades.objects.get(id = trade).bcurrency)
                    wal3.amount = wal.amount - amount
                    wal3.save()
                    amount = amount - item.amount
                    item.delete()
                    i = i +1
                    
            if amount > 0 :
                add = MainTradesSellOrder(trade = MainTrades.objects.get(id = trade) ,user = request.user, amount = amount , price = price, start = amountstart)
                add.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_201_CREATED)
        else:
            add = MainTradesSellOrder(trade = MainTrades.objects.get(id = trade) ,user = request.user, amount = amount , price = price , start = amountstart)
            add.save()
            return Response(status=status.HTTP_201_CREATED)

class maintradesinfo(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, id):
        return MainTrades.objects.get(id = id)

    def get(self , request, id, format=None):
        maintrade =  self.get_object(id)
        if len(MainTradesSellOrder.objects.filter(trade = maintrade).order_by('price')) > 0:
            minsell = MainTradesSellOrder.objects.filter(trade = maintrade).order_by('price')[0].price
        else:
            minsell = 0
        if len(MainTradesBuyOrder.objects.filter(trade = maintrade).order_by('-price')) > 0:
            maxbuy = MainTradesBuyOrder.objects.filter(trade = maintrade).order_by('-price')[0].price
        else:
            maxbuy = 0
        if(len(Wallet.objects.filter(user = request.user , currency = maintrade.scurrency))>0):
            sbalance = Wallet.objects.get(user = request.user , currency = maintrade.scurrency).amount
        else:
            sbalance = 0
        if(len(Wallet.objects.filter(user = request.user , currency = maintrade.bcurrency))>0):
            bbalance = Wallet.objects.get(user = request.user , currency = maintrade.bcurrency).amount
        else:
            bbalance = 0
        serializer = {'smin': minsell, 'bmax': maxbuy, 'sbalance': sbalance, 'bbalance': bbalance}
        print(serializer)
        return Response(serializer,status=status.HTTP_201_CREATED)

class maintradesselllist(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return ProTradesSellOrder.objects.filter(user = user)

    def get(self , request, format=None):
        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(request.user)
        serializer = ProTradesSellOrderSerializer(userinfo , many=True)
        return Response(serializer.data)

class maintradesbuylist(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return ProTradesBuyOrder.objects.filter(user = user)

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = ProTradesBuyOrderSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)


class protradebuyorders(APIView):

    def get_object(self , id):
        return ProTradesBuyOrder.objects.filter(trade = ProTrades.objects.get(id = id))

    def get(self, request, id, format=None):
        if len(self.get_object(id)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(id)
        serializer = ProTradesBuyOrderSerializer(userinfo , many=True)
        return Response(serializer.data)
    
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def post(self , request ,id , format=None):
        amount = float(request.data['amount'])
        amountstart = float(request.data['amount'])
        price = float(request.data['price'])
        trade = id
        user = request.user
        sells = ProTradesSellOrder.objects.filter(price__lte = request.data['price'] , trade = ProTrades.objects.get(id = id)).order_by('-price')
        i=0
        if amount * price > Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency).amount :
            return Response({
            'error' : "موجودی کافی نیست"
        }, status=status.HTTP_400_BAD_REQUEST)
        if len(sells) > 0 :
            while i < len(sells) or amount == 0:
                item = sells[i]
                if amount < item.amount :
                    if Wallet.objects.filter(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency):
                        wal = Wallet.objects.get(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency)
                        wal.amount = wal.amount + (amount * item.price)
                        wal.save()
                    else:
                        wal = Wallet(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency, amount = (amount * item.price))
                        wal.save()
                    if Wallet.objects.filter(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency):
                        wal2 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency)
                        wal2.amount = wal2.amount - (amount * item.price)
                        wal2.save()
                    else:
                        wal2 = Wallet(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency, amount = (amount * item.price))
                        wal2.save()
                    wal3 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                    wal3.amount = wal3.amount + amount
                    wal3.save()
                    amount = item.amount - amount
                    item.save()
                    amount = 0

                elif amount == item.amount :
                    if Wallet.objects.filter(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency):
                        wal = Wallet.objects.get(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency)
                        wal.amount = wal.amount + (amount * item.price)
                        wal.save()
                    else:
                        wal = Wallet(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency, amount = (amount * item.price))
                        wal.save()
                    if Wallet.objects.filter(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency):
                        wal2 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency)
                        wal2.amount = wal2.amount - (amount * item.price)
                        wal2.save()
                    else:
                        wal2 = Wallet(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency, amount = (amount * item.price))
                        wal2.save()
                    wal3 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                    wal3.amount = wal3.amount + amount
                    wal3.save()
                    item.delete()
                    amount = 0

                else :

                    if Wallet.objects.filter(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency):
                        wal = Wallet.objects.get(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency)
                        wal.amount = wal.amount + (amount * item.price)
                        wal.save()
                    else:
                        wal = Wallet(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency, amount = (amount * item.price))
                        wal.save()
                    if Wallet.objects.filter(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency):
                        wal2 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency)
                        wal2.amount = wal2.amount - (amount * item.price)
                        wal2.save()
                    else:
                        wal2 = Wallet(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency, amount = (amount * item.price))
                        wal2.save()
                    wal3 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                    wal3.amount = wal3.amount + amount
                    wal3.save()
                    amount = amount - item.amount
                    item.delete()
                    i = i +1
            if amount > 0 :
                add = ProTradesBuyOrder(trade = ProTrades.objects.get(id = trade) ,user = request.user, amount = amount , price = price , start = amountstart)
                add.save()
                wal3 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                wal3.amount = wal3.amount + amount
                wal3.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_201_CREATED)
        else:
            add = ProTradesBuyOrder(trade = ProTrades.objects.get(id = trade) ,user = request.user, amount = amount , price = price, start = amountstart)
            add.save()
            wal3 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency)
            wal3.amount = wal3.amount + amount
            wal3.save()
            return Response(status=status.HTTP_201_CREATED)
    

class protradesellorders(APIView):

    def get_object(self , id):
        return ProTradesSellOrder.objects.filter(trade = ProTrades.objects.get(id = id))

    def get(self, request, id, format=None):
        if len(self.get_object(id)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(id)
        serializer = ProTradesSellOrderSerializer(userinfo , many=True)
        return Response(serializer.data)
    
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def post(self , request, id , format=None):
        amount = float(request.data['amount'])
        amountstart = float(request.data['amount'])
        price = float(request.data['price'])
        trade = id
        user = request.user
        buys = ProTradesBuyOrder.objects.filter(price__gte = request.data['price'], trade = ProTrades.objects.get(id = trade)).order_by('price')
        i=0
        if amount > Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency).amount :
            return Response({
            'error' : "موجودی کافی نیست"
        }, status=status.HTTP_400_BAD_REQUEST)
        if len(buys) > 0 :
            while i < len(buys) or amount == 0:
                item = buys[i]
                if amount < item.amount :
                    if Wallet.objects.filter(user = item.user , currency = ProTrades.objects.get(id = trade).bcurrency):
                        wal = Wallet.objects.get(user = item.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                        wal.amount = wal.amount + amount
                        wal.save()
                    else:
                        wal = Wallet(user = item.user , currency = ProTrades.objects.get(id = trade).bcurrency, amount = amount)
                        wal.save()

                    if Wallet.objects.filter(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency):
                        wal2 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency)
                        wal2.amount = wal2.amount + (amount * item.price)
                        wal2.save()
                    else:
                        wal2 = Wallet(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency, amount = (amount * item.price))
                        wal2.save()
                    wal3 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                    wal3.amount = wal3.amount - amount
                    wal3.save()
                    item.amount = item.amount - amount
                    item.save()
                    amount = 0

                elif amount == item.amount :
                    if Wallet.objects.filter(user = item.user , currency = ProTrades.objects.get(id = trade).bcurrency):
                        wal = Wallet.objects.get(user = item.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                        wal.amount = wal.amount + amount
                        wal.save()
                    else:
                        wal = Wallet(user = item.user , currency = ProTrades.objects.get(id = trade).bcurrency, amount = amount)
                        wal.save()

                    if Wallet.objects.filter(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency):
                        wal2 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency)
                        wal2.amount = wal2.amount + (amount * item.price)
                        wal2.save()
                    else:
                        wal2 = Wallet(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency, amount = (amount * item.price))
                        wal2.save()
                    wal3 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                    wal3.amount = wal3.amount - amount
                    wal3.save()
                    item.delete()
                    amount = 0
                
                elif amount > item.amount :

                    if Wallet.objects.filter(user = item.user , currency = ProTrades.objects.get(id = trade).bcurrency):
                        wal = Wallet.objects.get(user = item.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                        wal.amount = wal.amount + amount
                        wal.save()
                    else:
                        wal = Wallet(user = item.user , currency = ProTrades.objects.get(id = trade).bcurrency, amount = amount)
                        wal.save()

                    if Wallet.objects.filter(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency):
                        wal2 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency)
                        wal2.amount = wal2.amount + (amount * item.price)
                        wal2.save()
                    else:
                        wal2 = Wallet(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency, amount = (amount * item.price))
                        wal2.save()
                    wal3 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                    wal3.amount = wal3.amount - amount
                    wal3.save()
                    amount = amount - item.amount
                    item.delete()
                    i = i +1
                    
            if amount > 0 :
                add = ProTradesSellOrder(trade = ProTrades.objects.get(id = trade) ,user = request.user, amount = amount , price = price, start = amountstart)
                add.save()
                wal3 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                wal3.amount = wal3.amount - amount
                wal3.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_201_CREATED)
        else:
            add = ProTradesSellOrder(trade = ProTrades.objects.get(id = trade) ,user = request.user, amount = amount , price = price , start = amountstart)
            add.save()
            wal3 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency)
            wal3.amount = wal3.amount - amount
            wal3.save()
            return Response(status=status.HTTP_201_CREATED)




class protradesinfo(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, id):
        return ProTrades.objects.get(id = id)

    def get(self , request, id, format=None):
        maintrade =  self.get_object(id)
        if len(ProTradesSellOrder.objects.filter(trade = maintrade).order_by('price')) > 0:
            minsell = ProTradesSellOrder.objects.filter(trade = maintrade).order_by('price')[0].price
        else:
            minsell = 0
        if len(ProTradesBuyOrder.objects.filter(trade = maintrade).order_by('-price')) > 0:
            maxbuy = ProTradesBuyOrder.objects.filter(trade = maintrade).order_by('-price')[0].price
        else:
            maxbuy = 0
        if(len(Wallet.objects.filter(user = request.user , currency = maintrade.scurrency))>0):
            sbalance = Wallet.objects.get(user = request.user , currency = maintrade.scurrency).amount
        else:
            sbalance = 0
        if(len(Wallet.objects.filter(user = request.user , currency = maintrade.bcurrency))>0):
            bbalance = Wallet.objects.get(user = request.user , currency = maintrade.bcurrency).amount
        else:
            bbalance = 0
        serializer = {'smin': minsell, 'bmax': maxbuy, 'sbalance': sbalance, 'bbalance': bbalance}
        print(serializer)
        return Response(serializer,status=status.HTTP_201_CREATED)

class protradesselllist(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return ProTradesSellOrder.objects.filter(user = user)

    def get(self , request, format=None):
        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(request.user)
        serializer = ProTradesSellOrderSerializer(userinfo , many=True)
        return Response(serializer.data)

class protradesbuylist(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return ProTradesBuyOrder.objects.filter(user = user)

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = ProTradesBuyOrderSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)




class fasttradesinfo(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self ,id):
        return MainTrades.objects.get(id = id)

    def get(self , request, id, format=None):
        maintrade =  self.get_object(id)
        maxsell = 0
        maxbuy = 0
        if len(MainTradesSellOrder.objects.filter(trade = maintrade).order_by('price')) > 0:
            for item in MainTradesSellOrder.objects.filter(trade = maintrade).order_by('price'):
                maxsell += item.amount
        if len(MainTradesBuyOrder.objects.filter(trade = maintrade).order_by('-price')) > 0:
            for itemm in MainTradesBuyOrder.objects.filter(trade = maintrade).order_by('-price'):
                maxbuy += item.amount
        if(len(Wallet.objects.filter(user = request.user , currency = maintrade.scurrency))>0):
            sbalance = Wallet.objects.get(user = request.user , currency = maintrade.scurrency).amount
        else:
            sbalance = 0
        if(len(Wallet.objects.filter(user = request.user , currency = maintrade.bcurrency))>0):
            bbalance = Wallet.objects.get(user = request.user , currency = maintrade.bcurrency).amount
        else:
            bbalance = 0        
        buymaintrades = MainTradesBuyOrderSerializer(MainTradesBuyOrder.objects.filter(trade = maintrade).order_by('-price'),many=True)
        sellmaintrades = MainTradesSellOrderSerializer(MainTradesSellOrder.objects.filter(trade = maintrade).order_by('price'),many=True)
        serializer = {'maxsell': maxsell, 'maxbuy': maxbuy, 'sbalance': sbalance, 'bbalance': bbalance, 'buymaintrades': buymaintrades.data,'sellmaintrades': sellmaintrades.data}
        return Response(serializer)

class indexprice(APIView):
    def get(self , request, format=None):
        response = requests.get('https://api.nomics.com/v1/currencies/ticker?key=5f176269caf5ea0dfab684904f9316bf1f4f2bc6&ids=BTC,ETH,TRX,DOGE,USDT')
        return HttpResponse(response) 

class indexhistory(APIView):
    def post(self , request, format=None):
        start = request.data['start']
        end = request.data['end']
        r = requests.get(f'https://api.nomics.com/v1/currencies/sparkline?key=5f176269caf5ea0dfab684904f9316bf1f4f2bc6&ids=BTC,ETH,TRX,DOGE,USDT&start={start}&end={end}')
        return HttpResponse(r) 
        

# < ------------   Margin Trades 


class oltradeinfo(APIView):
    def get(self , request, format=None):   
        list = {} 
        r = requests.get(url = 'https://api.coinex.com/v1/market/ticker/all')
        list = r.json()['data']['ticker']
        list2 = {}
        for item in Leverage.objects.all():
            list2[item.symbol] = list[item.symbol]
        return Response(list2)

class olboardinfo(APIView):
    def post(self , request, format=None):   
        coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
        return Response(coinex.market_depth(access_id='56255CA42286443EB7D3F6DB44633C25',market = request.data['sym'],tonce=time.time()*1000,))
        
class cp_balance(APIView):
    def post(self , request, format=None):   
        coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
        return Response(coinex.margin_account(access_id='56255CA42286443EB7D3F6DB44633C25',market =  request.data['sym'],tonce=time.time()*1000,))
        

class cp_mg_transfer(APIView):
    def get(self , request, format=None):   
        coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
        return Response(coinex.margin_transfer(from_account=0, to_account=27, coin_type='USDT', amount='23'))

class cp_pending(APIView):
    def post(self , request, format=None):   
        coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
        return Response(coinex.order_pending(market =  request.data['sym'],account_id=request.data['mid']))

class cp_stop_pending(APIView):
    def post(self , request, format=None):   
        coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
        return Response(coinex.order_stop_pending(market =  request.data['sym'],account_id=request.data['mid']))


class cp_close(APIView):
    def post(self , request, format=None):
        robot = CoinexPerpetualApi('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7')

        result = robot.close_market(
            request.data['market'],
            request.data['id']
        )
        return HttpResponse(json.dumps(result, indent=4))

class cp_finished(APIView):
    def post(self , request, format=None):   
        coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
        return Response(coinex.order_finished(market = request.data['sym'],account_id=request.data['mid']))


class cp_stop_finished(APIView):
    def post(self , request, format=None):   
        coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
        return Response(coinex.order_stop_finished(market = request.data['sym'],account_id=request.data['mid']))

class cp_transfer(APIView):
    def post(self , request):
        coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
        return Response(coinex.margin_transfer(from_account=request.data['from_account'], to_account=request.data['to_account'], coin_type=request.data['coin_type'] , amount=request.data['amount']))

class cp_market_order(APIView):
    def post(self , request):
        coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
        return Response(coinex.order_market(account_id=request.data['mid'],access_id='56255CA42286443EB7D3F6DB44633C25',market = request.data['market'],type=request.data['type'],amount=request.data['amount'],tonce=time.time()*1000,))
        

class cp_limit_order(APIView):
    def post(self , request):
        coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
        return Response(coinex.order_limit(account_id=request.data['mid'],access_id='56255CA42286443EB7D3F6DB44633C25',market = request.data['market'],type=request.data['type'],amount=request.data['amount'],price=request.data['price'],tonce=time.time()*1000,))


class cp_stop_limit_order(APIView):
    def post(self , request):
        coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
        return Response(coinex.order_stop_limit(account_id=request.data['mid'],access_id='56255CA42286443EB7D3F6DB44633C25',market = request.data['market'],type=request.data['type'],amount=request.data['amount'],price=request.data['price'],stop_price=request.data['stop_price'],tonce=time.time()*1000,))



class cp_cancel_order(APIView):
    def post(self , request):
        coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
        return Response(coinex.order_pending_cancel(market = request.data['market'],id = request.data['id']))
        
class cp_stop_cancel_order(APIView):
    def post(self , request):
        coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
        return Response(coinex.order_stop_pending_cancel( account_id=request.data['mid'],market = request.data['market'],id = request.data['id']))
        
class cp_mg_market(APIView):
    def get(self , request):
        r = requests.get('https://api.coinex.com/v1/margin/market')
        r = r.json()
        result = []
        for item in r['data'] :
            if 'USDT' in item :
                result.append([item, r['data'][item]])
        return Response(result)

class cp_mg_usdt(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def get(self , request):
        usdt = Wallet.objects.filter( Q(user = request.user, currency = Currencies.objects.get(id = 4)) | Q(user = request.user, currency = Currencies.objects.get(id = 41)))
        serializer = WalletSerializer(usdt , many = True)
        return Response(serializer.data)


class cp_mg_main(APIView):
    def get(self , request):
        coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
        return HttpResponse(coinex.balance_info()['USDT']['available'])
        

#  Margin Trades ------------ >


#  < ------------ Perpetual Trades 



class olptradeinfo(APIView):
    def get(self , request, format=None):   
        robot = CoinexPerpetualApi('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7')

        result = {}
        tick = robot.tickers()
        for key in tick['data']['ticker']:
            if not '_' in key and 'USDT' in key :
                result[f'{key}'] = tick['data']['ticker'][key]['last']
        return Response(result)

class olpboardinfo(APIView):
    def post(self , request, format=None):   
        robot = CoinexPerpetualApi('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7')

        result = robot.depth(market = request.data['sym'])
        return Response(result)
        
class cpp_balance(APIView):
    def post(self , request, format=None):   
        robot = CoinexPerpetualApi('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7')

        result = robot.query_account()
        return Response(result)

class cpp_mg_transfer(APIView):
    def get(self , request, format=None):   
        coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
        return Response(coinex.margin_transfer(from_account=0, to_account=request.data['mid'], coin_type='USDT', amount='23'))

class cpp_pending(APIView):
    def post(self , request, format=None):   
        robot = CoinexPerpetualApi('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7')

        result = robot.query_order_pending(market=request.data['sym'], side = 0, offset=False)
        return Response(result)


class cpp_stop_pending(APIView):
    def post(self , request, format=None):   
        robot = CoinexPerpetualApi('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7')

        result = robot.query_stop_pending(market=request.data['sym'], side = 0, offset=False)
        return Response(result)

class cpp_close(APIView):
    def post(self , request, format=None):
        robot = CoinexPerpetualApi('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7')

        result = robot.close_market(
            request.data['market'],
            request.data['id']
        )
        return HttpResponse(json.dumps(result, indent=4))

class cpp_finished(APIView):
    def post(self , request, format=None):   
        robot = CoinexPerpetualApi('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7')

        result = robot.query_order_finished(market=request.data['sym'], side = 0, offset=False)
        return Response(result)

class cpp_stop_finished(APIView):
    def post(self , request, format=None):   
        robot = CoinexPerpetualApi('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7')

        result = robot.query_stop_finished(market=request.data['sym'], side = 0, offset=False)
        return Response(result)


class cpp_transfer(APIView):
    def get(self , request):
        coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
        return Response(coinex.margin_account(access_id='56255CA42286443EB7D3F6DB44633C25',market = 'TRXUSDT',tonce=time.time()*1000,))



class cpp_market_order(APIView):
    def post(self , request):
        robot = CoinexPerpetualApi('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7')

        result = robot.put_market_order(market=request.data['sym'], amount= request.data['amount'], side=request.data['type'])
        return Response(result)


class cpp_limit_order(APIView):
    def post(self , request):
        robot = CoinexPerpetualApi('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7')

        result = robot.put_limit_order(market = request.data['market'],side=request.data['type'],amount=request.data['amount'],price=request.data['price'])
        return Response(result)


class cpp_stop_limit_order(APIView):
    def post(self , request):
        robot = CoinexPerpetualApi('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7')

        result = robot.put_stop_limit_order(market = request.data['market'],side=request.data['type'],amount=request.data['amount'],price=request.data['price'],stop_price=request.data['stop_price'])
        return Response(result)



class cpp_cancel_order(APIView):
    def post(self , request):
        robot = CoinexPerpetualApi('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7')

        result = robot.close_market(market = request.data['market'],id = request.data['id'])
        return Response(result)




# Moms



class olmtradeinfo(APIView):
    def get(self , request, format=None):   
        robot = CoinexPerpetualApi('641A03D0C52B4CE89EC78A77D0289E42', 'BC17D99BA712F09B084DB940F78AEE3CD18826C1CFA05EAF')

        result = {}
        tick = robot.tickers()
        for key in tick['data']['ticker']:
            if not '_' in key and 'USDT' in key :
                result[f'{key}'] = tick['data']['ticker'][key]['last']
        return Response(result)

class olmboardinfo(APIView):
    def post(self , request, format=None):   
        robot = CoinexPerpetualApi('641A03D0C52B4CE89EC78A77D0289E42', 'BC17D99BA712F09B084DB940F78AEE3CD18826C1CFA05EAF')

        result = robot.depth(market = request.data['sym'])
        return Response(result)
        
class cpm_balance(APIView):
    def post(self , request, format=None):   
        robot = CoinexPerpetualApi('641A03D0C52B4CE89EC78A77D0289E42', 'BC17D99BA712F09B084DB940F78AEE3CD18826C1CFA05EAF')

        result = robot.query_account()
        return Response(result)

class cpm_mg_transfer(APIView):
    def get(self , request, format=None):   
        coinex = CoinEx('641A03D0C52B4CE89EC78A77D0289E42', 'BC17D99BA712F09B084DB940F78AEE3CD18826C1CFA05EAF' )
        return Response(coinex.margin_transfer(from_account=0, to_account=request.data['mid'], coin_type='USDT', amount='23'))

class cpm_pending(APIView):
    def post(self , request, format=None):   
        robot = CoinexPerpetualApi('641A03D0C52B4CE89EC78A77D0289E42', 'BC17D99BA712F09B084DB940F78AEE3CD18826C1CFA05EAF')

        result = robot.query_order_pending(market=request.data['sym'], side = 0, offset=False)
        return Response(result)


class cpm_stop_pending(APIView):
    def post(self , request, format=None):   
        robot = CoinexPerpetualApi('641A03D0C52B4CE89EC78A77D0289E42', 'BC17D99BA712F09B084DB940F78AEE3CD18826C1CFA05EAF')

        result = robot.query_stop_pending(market=request.data['sym'], side = 0, offset=False)
        return Response(result)

class cpm_close(APIView):
    def post(self , request, format=None):
        robot = CoinexPerpetualApi('641A03D0C52B4CE89EC78A77D0289E42', 'BC17D99BA712F09B084DB940F78AEE3CD18826C1CFA05EAF')

        result = robot.close_market(
            request.data['market'],
            request.data['id']
        )
        return HttpResponse(json.dumps(result, indent=4))

class cpm_finished(APIView):
    def post(self , request, format=None):   
        robot = CoinexPerpetualApi('641A03D0C52B4CE89EC78A77D0289E42', 'BC17D99BA712F09B084DB940F78AEE3CD18826C1CFA05EAF')

        result = robot.query_order_finished(market=request.data['sym'], side = 0, offset=False)
        return Response(result)

class cpm_stop_finished(APIView):
    def post(self , request, format=None):   
        robot = CoinexPerpetualApi('641A03D0C52B4CE89EC78A77D0289E42', 'BC17D99BA712F09B084DB940F78AEE3CD18826C1CFA05EAF')

        result = robot.query_stop_finished(market=request.data['sym'], side = 0, offset=False)
        return Response(result)


class cpm_transfer(APIView):
    def get(self , request):
        coinex = CoinEx('641A03D0C52B4CE89EC78A77D0289E42', 'BC17D99BA712F09B084DB940F78AEE3CD18826C1CFA05EAF' )
        return Response(coinex.margin_account(access_id='641A03D0C52B4CE89EC78A77D0289E42',market = 'TRXUSDT',tonce=time.time()*1000,))



class cpm_market_order(APIView):
    def post(self , request):
        robot = CoinexPerpetualApi('641A03D0C52B4CE89EC78A77D0289E42', 'BC17D99BA712F09B084DB940F78AEE3CD18826C1CFA05EAF')

        result = robot.put_market_order(market=request.data['sym'], amount= request.data['amount'], side=request.data['type'])
        return Response(result)


class cpm_limit_order(APIView):
    def post(self , request):
        robot = CoinexPerpetualApi('641A03D0C52B4CE89EC78A77D0289E42', 'BC17D99BA712F09B084DB940F78AEE3CD18826C1CFA05EAF')

        result = robot.put_limit_order(market = request.data['market'],side=request.data['type'],amount=request.data['amount'],price=request.data['price'])
        return Response(result)


class cpm_stop_limit_order(APIView):
    def post(self , request):
        robot = CoinexPerpetualApi('641A03D0C52B4CE89EC78A77D0289E42', 'BC17D99BA712F09B084DB940F78AEE3CD18826C1CFA05EAF')

        result = robot.put_stop_limit_order(market = request.data['market'],side=request.data['type'],amount=request.data['amount'],price=request.data['price'],stop_price=request.data['stop_price'])
        return Response(result)



class cpm_cancel_order(APIView):
    def post(self , request):
        robot = CoinexPerpetualApi('641A03D0C52B4CE89EC78A77D0289E42', 'BC17D99BA712F09B084DB940F78AEE3CD18826C1CFA05EAF')

        result = robot.close_market(market = request.data['market'],id = request.data['id'])
        return Response(result)