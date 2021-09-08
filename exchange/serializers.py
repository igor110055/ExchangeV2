from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import  Leverage, MainTradesBuyOrder, MainTradesSellOrder, ProTradesBuyOrder, ProTradesSellOrder , ProTrades , MainTrades, Notification , VerifyMelliRequest , BankAccounts , VerifyBankAccountsRequest , Price , Currencies, Forgetrequest, UserInfo, Wallet, Verify, BankCards, Transactions, Settings , Subjects , Tickets, Pages, VerifyBankRequest, Staff

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = (
            "id",
            "first_name",
            "last_name",
            "mobile",
            "email",
            "level",
            "is_active",
            "is_admin"
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

class LeverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leverage
        fields = (
            "symbol",
            "leverage",
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
            "address",
            "address2",
            "get_currency"
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
            "mobilev",
            "emailv",
            "melliv",
            "bankv"
        )


class VerifyMelliRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyMelliRequest
        fields = (
            "id",
            "user",
            "melliimg",
            "mellic",
            "action",
            "get_image",
            "get_user"
        )


class BankCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankCards
        fields = (
            "user",
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
            "bankc",
            "get_user",
            "action"
        )

class VerifyBankAccountsRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyBankAccountsRequest
        fields = (
            "id",
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
            "id",
            "date",
            "user",
            "act",
            "read",
            "title",
            "aread",
            "get_age",
            "get_lastticket"
        )
class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = (
            "date",
            "subid",
            "text",
            "get_age",
            "get_title",
            "get_user"
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

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            "title",
            "text",
            "seen",
            "get_age",
        )

class MainTradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainTrades
        fields = (
            "id",
            "name",
            "brand",
            "get_bname",
            "get_sname"
        )

class ProTradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProTrades
        fields = (
            "id",
            "name",
            "brand",
        )

class ProTradesSellOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProTradesSellOrder
        fields = (
            "trade",
            "amount",
            "price",
            "start",
            "date",
            "get_age",
            "get_brand"
        )

class ProTradesBuyOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProTradesBuyOrder
        fields = (
            "trade",
            "amount",
            "price",
            "start",
            "date",
            "get_age",
            "get_brand"
        )

class MainTradesSellOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainTradesSellOrder
        fields = (
            "trade",
            "amount",
            "price",
            "start",
            "date",
            "get_age",
            "get_brand"
        )

class MainTradesBuyOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainTradesBuyOrder
        fields = (
            "trade",
            "amount",
            "price",
            "start",
            "date",
            "get_age",
            "get_brand"
        )