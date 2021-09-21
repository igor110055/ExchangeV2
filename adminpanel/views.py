from typing import Text
from exchange.views import cp_withdraw, currencies, currency, notifications, price, usersinfo
from django.shortcuts import get_object_or_404, render
from django import http
from django.db.models.fields import EmailField
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from rest_framework import request, serializers
from django.http import HttpResponse , Http404 
from rest_framework import status
from rest_framework import authentication
from exchange.serializers import  BottomStickerSerializer, Cp_WithdrawSerializer, CpWalletSerializer, GeneralSerializer, PerpetualRequestSerializer, PostsSerializer, TopStickerSerializer, VerifyMelliRequest , BankAccountsSerializer, StaffSerializer, UserInfoSerializer, VerifyBankAccountsRequestSerializer, VerifyMelliRequestSerializer , WalletSerializer , CurrenciesSerializer ,VerifySerializer, BankCardsSerializer, TransactionsSerializer, SettingsSerializer, SubjectsSerializer, TicketsSerializer, PagesSerializer , UserSerializer , ForgetSerializer, VerifyBankRequestSerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from exchange.models import BottomSticker, Cp_Withdraw, General, News, Notification, Perpetual, PerpetualRequest, Posts ,  Price, Staff, TopSticker,  UserInfo , Currencies, VerifyBankAccountsRequest, VerifyBankRequest, VerifyMelliRequest , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
from django.contrib.auth.models import AbstractUser , User
from django.contrib.auth.decorators import user_passes_test
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from py_crypto_hd_wallet import HdWalletFactory, HdWalletCoins, HdWalletSpecs , HdWalletWordsNum
import json
from datetime import datetime ,timedelta
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from ippanel import Client
import pytz
from random import randrange

def email(user , date , title , text) :
    send_mail(
        'Subject here',
        f'به شرکت سرمایه گذاری ... خوش آمدید کد فعالسازی : {"vcode"} ',
        'info@ramabit.com',
        [f'armansaheb@gmail.com'],
        fail_silently=False,
    )

def sms(user , date , title  , text ):
    sms = Client("HpmWk_fgdm_OnxGYeVpNE1kmL8fTKC7Fu0cuLmeXQHM=")

    pattern_values = {
    "verification-code": f"dcsdcdscd",
    }

    bulk_id = sms.send_pattern(
        "pifmmqr30d",    # pattern code
        "+983000505",      # originator
        f"+989999999",  # recipient
        pattern_values,  # pattern values
    )

    message = sms.get_message(bulk_id)
    print(message)
    print(f"+98999999999")
    return True

def notification (user , date = datetime.now(), title = '' , text = ''):
    note = Notification(user = user , title = title , text = text)
    note.save()
    sms(user , date, title, text)
    email(user , date, title, text)

class staff(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get_object(self , user):
        try:
            return Staff.objects.filter(user = user)
        except UserInfo.DoesNotExist:
            return Http404

    def get(self , request , format=None):
        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        staff =  self.get_object(request.user)
        serializer = StaffSerializer(staff , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        if Staff.objects.get(user = request.user).level < 3 :
            return Response(status= status.HTTP_400_BAD_REQUEST)
        if len(Staff.objects.filter(user = request.user))<1:
            serializer = StaffSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.error, status= status.HTTP_400_BAD_REQUEST)
        else:
            serializer = Staff.objects.get(user = request.data['id'])
            serializer.level = request.data['level']
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class user(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        users = []
        userinfo =  User.objects.all()
        for item in userinfo :
            if len(UserInfo.objects.filter(user = item)) > 0:
                userinfos = UserInfo.objects.get(user = item)
                wallet= 0
                price = 0
                for itemm in Wallet.objects.filter(user = item):
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
                users.append({'username': item.username, 'level': userinfos.level, 'balance': wallet, 'is_active': userinfos.is_active, 'is_admin': userinfos.is_admin, 'id': item.id })
        return Response(users)
    def post(self , request , format=None):
        user = UserInfo.objects.get(user = User.objects.get(id = request.data['id']))
        if request.data['act'] == 1:
            if user.is_active == True:
                user.is_active = False
            elif user.is_active == False:
                user.is_active = True
        user.save()
        return Response(status=status.HTTP_201_CREATED)

class bankcards(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        bankcards = VerifyBankRequest.objects.all()
        serializer = VerifyBankRequestSerializer(bankcards , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response({'message': 'not admin'}, status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response({'message': 'not admin'}, status= status.HTTP_400_BAD_REQUEST)
        request.data['user'] = VerifyBankRequest.objects.get(id = request.data['id']).user.id
        serializer = BankCardsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            VerifyBankRequest.objects.get(id = request.data['id']).delete()
            verify = Verify.objects.get(user = request.data['user'])
            verify.bankv = True
            verify.save()
            if verify.bankv and verify.melliv and verify.mobilev and verify.emailv :
                user = UserInfo.objects.get(user = request.data['user'])
                user.level = 1
                user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        id = request.data['id']
        req = VerifyBankRequest.objects.get(id = id)
        req.delete()
        return Response(status=status.HTTP_201_CREATED)

class bankaccounts(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        bankcards = VerifyBankAccountsRequest.objects.all()
        serializer = VerifyBankAccountsRequestSerializer(bankcards , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        serializer = BankAccountsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            id = request.data['id']
            req = VerifyBankAccountsRequest.objects.get(id = id)
            req.delete()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        id = request.data['id']
        req = VerifyBankAccountsRequest.objects.get(id = id)
        req.delete()
        return Response(status=status.HTTP_201_CREATED)

class verifymelli(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        bankcards = VerifyMelliRequest.objects.all()
        serializer = VerifyMelliRequestSerializer(bankcards , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        verify = Verify.objects.get(user = request.data['user'])
        verify.melliv = True
        verify.save()
        if verify.bankv and verify.melliv and verify.mobilev and verify.emailv :
            user = UserInfo.objects.get(user = request.data['user'])
            user.level = 1
            user.save()
        id = request.data['id']
        req = VerifyMelliRequest.objects.get(id = id)
        req.delete()
        return Response(status=status.HTTP_201_CREATED)
 
    def put(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        no = request.data['number']
        req = VerifyMelliRequest.objects.get(mellic = no)
        req.delete()
        return Response(status=status.HTTP_201_CREATED)


class cwithdraw(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        bankcards = Cp_Withdraw.objects.filter(rejected = False , completed = False)
        serializer = Cp_WithdrawSerializer(bankcards , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        id = request.data['id']
        req = Cp_Withdraw.objects.get(id = id)
        user = req.user.id
        notification(user = User.objects.get(id = user) , title = 'درخواست برداشت وجه شما انجام شد' , text = f'درخواست برداشت مقدار  {req.amount} و ارسال آن به آدرس  {req.address} با موفقیت انجام شد ')
        req.completed = True
        req.save()
        return Response(status=status.HTTP_201_CREATED)
 
    def put(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        id = request.data['id']
        req = Cp_Withdraw.objects.get(id = id)
        user = req.user.id
        notification(user = User.objects.get(id = user) , title = ' متاسفانه درخواست برداشت وجه شما انجام نشد ' , text = f'درخواست برداشت مقدار  {req.amount} و ارسال آن به آدرس  {req.address}  با مشکل روبرو شد . لطفا با پشتیبانی تماس بگیرید ')
        req.rejected = True
        req.save()
        return Response(status=status.HTTP_201_CREATED)

class rcwithdraw(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        bankcards = Cp_Withdraw.objects.filter(rejected = True)
        serializer = Cp_WithdrawSerializer(bankcards , many=True)
        return Response(serializer.data)

class ccwithdraw(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        bankcards = Cp_Withdraw.objects.filter(completed = True)
        serializer = Cp_WithdrawSerializer(bankcards , many=True)
        return Response(serializer.data)


class general(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        query = General.objects.filter(id = 1)
        serializer = GeneralSerializer(query , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        gen = General.objects.get(id = 1)
        if 'name' in request.data :
            gen.name = request.data['name']
        if 'email' in request.data :
            gen.email = request.data['email']
        if 'telephone' in request.data :
            gen.telephone = request.data['telephone']
        if 'instagram' in request.data :
            gen.instagram = request.data['instagram']
        if 'telegram' in request.data :
            gen.telegram = request.data['telegram']
        if 'whatsapp' in request.data :
            gen.whatsapp = request.data['whatsapp']
        if 'rule' in request.data :
            gen.rule = request.data['rule']
        if 'logo' in request.data :
            gen.logo = request.data['logo']
        gen.save()
        return Response(status=status.HTTP_201_CREATED)

class perpetualreq(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        query = PerpetualRequest.objects.all()
        serializer = PerpetualRequestSerializer(query , many=True)
        return Response(serializer.data)

    def post(self , request, id , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        query = PerpetualRequest.objects.filter(id = id)
        serializer = PerpetualRequestSerializer(query , many=True)
        return Response(serializer.data)

class perpetualreqccept(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        id = request.data['id']
        user = PerpetualRequest.objects.get(id = id).user
        print(request.data['name'])
        per = Perpetual(user = user ,name = request.data['name'], apikey = request.data['apikey'] , secretkey = request.data['secretkey'])
        per.save()
        PerpetualRequest.objects.filter(id = id).delete()
        return Response(status=status.HTTP_201_CREATED)


class subject(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self , user):
        return Subjects.objects.all()

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)

        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(request.user)
        serializer = SubjectsSerializer(userinfo , many=True)
        return Response(serializer.data)

    def post(self, request, id, format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)

        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  Subjects.objects.filter(id = id)
        serializer = SubjectsSerializer(userinfo , many=True)
        return Response(serializer.data)

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

class topsticker(APIView):
    def post(self , request , format=None):
        serializer = TopStickerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request , format=None):
        serializer = TopSticker.objects.get(id=request.data['id'])
        serializer.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class bottomsticker(APIView):
    def post(self , request , format=None):
        serializer = BottomStickerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request , format=None):
        serializer = BottomSticker.objects.get(id=request.data['id'])
        serializer.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class posts(APIView):
    def post(self , request , format=None):
        serializer = PostsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request , format=None):
        serializer = Posts.objects.get(id=request.data['id'])
        serializer.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class news(APIView):
    def post(self , request , format=None):
        serializer = News(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request , format=None):
        serializer = News.objects.get(id=request.data['id'])
        serializer.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class pages(APIView):
    def post(self , request , format=None):
        serializer = Pages(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request , format=None):
        serializer = Pages.objects.get(id=request.data['id'])
        serializer.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)