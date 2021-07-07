from django.shortcuts import render
from django import http
from django.db.models.fields import EmailField
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from rest_framework import request, serializers
from django.http import HttpResponse , Http404 
from rest_framework import status
from rest_framework import authentication
from exchange.serializers import VerifyMelliRequest , BankAccountsSerializer, StaffSerializer, UserInfoSerializer, VerifyBankAccountsRequestSerializer, VerifyMelliRequestSerializer , WalletSerializer , CurrenciesSerializer ,VerifySerializer, BankCardsSerializer, TransactionsSerializer, SettingsSerializer, SubjectsSerializer, TicketsSerializer, PagesSerializer , UserSerializer , ForgetSerializer, VerifyBankRequestSerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from exchange.models import Staff,  UserInfo , Currencies, VerifyBankAccountsRequest, VerifyBankRequest, VerifyMelliRequest , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages, Mainwalls , Forgetrequest
from django.contrib.auth.models import AbstractUser , User
from django.contrib.auth.decorators import user_passes_test
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from pywallet import wallet as wall
from py_crypto_hd_wallet import HdWalletFactory, HdWalletCoins, HdWalletSpecs , HdWalletWordsNum
import json
from datetime import datetime ,timedelta
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from ippanel import Client
import pytz
from random import randrange



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
        if Staff.objects.get(user = request.user.id).level < 3 :
            return Response(status= status.HTTP_400_BAD_REQUEST)
        if len(Staff.objects.filter(user = request.user.id))<1:
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

class bankcards(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user.id))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user.id).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        bankcards = VerifyBankRequest.objects.all()
        serializer = VerifyBankRequestSerializer(bankcards , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        if len(Staff.objects.filter(user = request.user.id))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user.id).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        serializer = BankCardsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self , request , format=None):
        if len(Staff.objects.filter(user = request.user.id))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user.id).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        no = request.data['number']
        req = VerifyBankRequest.objects.get(bankc = no)
        req.delete()
        return Response(status=status.HTTP_201_CREATED)

class bankaccounts(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user.id))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user.id).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        bankcards = VerifyBankAccountsRequest.objects.all()
        print(bankcards[0].bankc)
        serializer = VerifyBankAccountsRequestSerializer(bankcards , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        if len(Staff.objects.filter(user = request.user.id))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user.id).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        serializer = BankAccountsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            no = request.data['number']
            req = VerifyBankAccountsRequest.objects.get(bankc = no)
            req.delete()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self , request , format=None):
        if len(Staff.objects.filter(user = request.user.id))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user.id).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        no = request.data['number']
        req = VerifyBankAccountsRequest.objects.get(bankc = no)
        req.delete()
        return Response(status=status.HTTP_201_CREATED)

class verifymelli(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user.id))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user.id).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        bankcards = VerifyMelliRequest.objects.all()
        serializer = VerifyMelliRequestSerializer(bankcards , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        if len(Staff.objects.filter(user = request.user.id))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user.id).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        verify = Verify.objects.get(user = request.data['user'])
        verify.melliv = True
        verify.save()
        no = request.data['number']
        req = VerifyMelliRequest.objects.get(mellic = no)
        req.delete()
        return Response(status=status.HTTP_201_CREATED)

    def put(self , request , format=None):
        if len(Staff.objects.filter(user = request.user.id))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user.id).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        no = request.data['number']
        req = VerifyMelliRequest.objects.get(mellic = no)
        req.delete()
        return Response(status=status.HTTP_201_CREATED)

class bankrequests(APIView):
    def get_object(self , user):
        try:
            return VerifyBankRequest.objects.filter(user = user)
        except UserInfo.DoesNotExist:
            return Http404

    def get(self , request , format=None):
        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(request.user)
        serializer = VerifyBankRequestSerializer(userinfo , many=True)
        return Response(serializer.data)