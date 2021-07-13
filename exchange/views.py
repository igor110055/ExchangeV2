from typing import Text
from django import http
from django.db.models.fields import EmailField
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from rest_framework import request, serializers
from django.http import HttpResponse , Http404 
from rest_framework import status
from rest_framework import authentication
from .serializers import MainTradesBuyOrderSerializer, MainTradesSellOrderSerializer, ProTradesSerializer, MainTradesSerializer, NotificationSerializer, BankAccountsSerializer, VerifyBankAccountsRequest , PriceSerializer , StaffSerializer, UserInfoSerializer, VerifyBankAccountsRequestSerializer, VerifyMelliRequestSerializer , WalletSerializer , CurrenciesSerializer ,VerifySerializer, BankCardsSerializer, TransactionsSerializer, SettingsSerializer, SubjectsSerializer, TicketsSerializer, PagesSerializer , UserSerializer , ForgetSerializer, VerifyBankRequestSerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from .models import ProTradesSellOrder, MainTradesSellOrder,ProTradesBuyOrder, MainTradesBuyOrder, ProTrades, MainTrades, Notification , VerifyBankAccountsRequest , BankAccounts, Price, Staff,  UserInfo , Currencies, VerifyMelliRequest , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages, Mainwalls , Forgetrequest , VerifyBankRequest
from django.contrib.auth.models import AbstractUser , User
from django.contrib.auth.decorators import user_passes_test
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from pywallet import wallet as wall
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
            note = Notification(user = request.user , title = 'خوش آمدید' , text = 'به ... خوش آمدید') 
            note.save()
        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(request.user)
        serializer = UserInfoSerializer(userinfo , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        request.data['user'] = request.user.id
        serializer = UserInfoSerializer(data=request.data)
        if serializer.is_valid():
            if len(UserInfo.objects.filter(user = request.user.id))<1:
                serializer.save()
                note = Notification(user = request.user , title = ' اطلاعات شما با موفقیت ثبت شد' , text = 'برای شروع معاملات لطفا احراز هویت را انجام دهید') 
                note.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                user = UserInfo.objects.get(user = request.user.id)
                user.first_name = request.data['first_name']
                user.last_name = request.data['last_name']
                user.mobile = request.data['mobile']
                user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            wa = Wallet(user = request.user , currency = Currencies.objects.get(id = id) , amount = 0 , address = address , key = key)
            wa.save()
            return Response({status:200})
        if id == 2 :
#            hd_wallet = Mainwalls.objects.get(currency = id).wall
#            address = hd_wallet['addresses'][f'address_{request.user.id}']['address']
#            key = hd_wallet['addresses'][f'address_{request.user.id}']['wif_priv']
#            wa = Wallet(user = request.user , currency = Currencies.objects.get(id = id) , amount = 0 , address = address , key = key)
#            wa.save()
#            return Response({status:200})
            hd_wallet_fact = HdWalletFactory(HdWalletCoins.BITCOIN_TESTNET)
            hd_wallet = hd_wallet_fact.CreateRandom("my_wallet_name", HdWalletWordsNum.WORDS_NUM_12)
            hd_wallet.Generate(addr_num = 1)
            wallet_data = hd_wallet.ToDict()
            address = wallet_data['addresses']['address_1']['address']
            key = wallet_data['addresses']['address_1']['raw_priv']
            wa = Wallet(user = request.user , currency = Currencies.objects.get(id = id) , amount = 0 , address = address , key = key)
            wa.save()
            return Response(status=status.HTTP_201_CREATED)


        if id == 3 :
            hd_wallet = Mainwalls.objects.get(currency = id).wall
            address = hd_wallet['addresses'][f'address_{request.user.id}']['address']
            key = hd_wallet['addresses'][f'address_{request.user.id}']['raw_priv']
            wa = Wallet(user = request.user , currency = Currencies.objects.get(id = id) , amount = 0 , address = address , key = key)
            wa.save()
            return Response({status:200})
        if id == 6 :
            hd_wallet = Mainwalls.objects.get(currency = id).wall
            address = hd_wallet['addresses'][f'address_{request.user.id}']['address']
            key = hd_wallet['addresses'][f'address_{request.user.id}']['wif_priv']
            wa = Wallet(user = request.user , currency = Currencies.objects.get(id = id) , amount = 0 , address = address , key = key)
            wa.save()
            return Response({status:200})



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
            f'لینک بازیابی رمز عبور شما : http://127.0.0.1:8000/api/v1/resetpass/{key} ',
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
        user = Verify.objects.get(user= request.user)
        vcode = randrange(123456,999999)
        user.mobilec = vcode
        user.save()

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
        if(int(request.data['code']) == int(user.mobilec)):
            user.mobilev = True
            user.save()
            if(len(UserInfo.objects.filter(user=request.user))<1):
                userinfo = UserInfo(user=request.user , mobile= request.data['mobile'])
                userinfo.save()
            else:
                userinfo = UserInfo.objects.get(user=request.user)
                userinfo.mobile = request.data['mobile']
                userinfo.save()
            if (user.melliv == 3 and user.emailv == True ):
                per = UserInfo.objects.get(user = request.user)
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
            while i < len(sells):
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
                add = MainTradesBuyOrder(trade = MainTrades.objects.get(id = trade) ,user = request.user, amount = amount , price = price)
                add.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_201_CREATED)
        else:
            add = MainTradesBuyOrder(trade = MainTrades.objects.get(id = trade) ,user = request.user, amount = amount , price = price)
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
            while i < len(buys):
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
                
                else :

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
                add = MainTradesSellOrder(trade = MainTrades.objects.get(id = trade) ,user = request.user, amount = amount , price = price)
                add.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_201_CREATED)
        else:
            add = MainTradesSellOrder(trade = MainTrades.objects.get(id = trade) ,user = request.user, amount = amount , price = price)
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
        sbalance = Wallet.objects.get(user = request.user , currency = maintrade.scurrency).amount
        bbalance = Wallet.objects.get(user = request.user , currency = maintrade.bcurrency).amount
        serializer = {'smin': minsell, 'bmax': maxbuy, 'sbalance': sbalance, 'bbalance': bbalance}
        print(serializer)
        return Response(serializer)

class fasttradesbuyinfo(APIView):
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
        sbalance = Wallet.objects.get(user = request.user , currency = maintrade.scurrency).amount
        bbalance = Wallet.objects.get(user = request.user , currency = maintrade.bcurrency).amount
        serializer = {'smin': minsell, 'bmax': maxbuy, 'sbalance': sbalance, 'bbalance': bbalance}
        print(serializer)
        return Response(serializer)
    
class fasttradessellinfo(APIView):
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
        sbalance = Wallet.objects.get(user = request.user , currency = maintrade.scurrency).amount
        bbalance = Wallet.objects.get(user = request.user , currency = maintrade.bcurrency).amount
        serializer = {'smin': minsell, 'bmax': maxbuy, 'sbalance': sbalance, 'bbalance': bbalance}
        print(serializer)
        return Response(serializer)