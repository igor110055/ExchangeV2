from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import BankAccounts , VerifyBankAccountsRequest , Price , Currencies, Forgetrequest, UserInfo, Wallet, Verify, BankCards, Transactions, Settings , Subjects , Tickets, Pages, VerifyBankRequest, Staff

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = (
            "id",
            "user",
            "first_name",
            "last_name",
            "mobile",
            "level"
        )

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = (
            "rial",
            "btc",
            "eth",
            "trx",
            "usdt",
            "doge",
            "usd",
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = (
            "id",
            "currency",
            "amount",
            "address"
        )
class CurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currencies
        fields = (
            "id",
            "name",
            "brand",
            "get_image"
        )

class VerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Verify
        fields = (
            "mobileverify",
            "emailverify",
            "melliverify",
            "bankverify"
        )
class BankCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankCards
        fields = (
            "user",
            "image",
            "number",
            "status"
        )

class BankAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccounts
        fields = (
            "user",
            "number",
            "status"
        )

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = (
            "user",
            "level",
        )

class VerifyBankRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyBankRequest
        fields = (
            "id",
            "user",
            "bankimg",
            "bankc",
            "get_image",
            "get_user",
            "action"
        )

class VerifyBankAccountsRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyBankAccountsRequest
        fields = (
            "user",
            "bankc",
            "get_user",
            "action"
        )

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = (
            "date",
            "amount",
            "user",
            "currency",
            "act"
        )


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = (
            "id",
            "name",
            "address",
            "tel",
            "email",
            "telegram",
            "whatsapp",
            "instagram",
            "facebook",
            "logo"
        )

class SubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = (
            "date",
            "lastdate",
            "user",
            "act",
            "read",
            "title",
            "aread",
        )
class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = (
            "date",
            "subid",
            "text",
            "pic",
        )


class PagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pages
        fields = (
            "name",
            "title",
            "text",
        )
class ForgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forgetrequest
        fields = (
            "email",
        )