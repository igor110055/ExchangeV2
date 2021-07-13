from django.contrib import admin
from django.core import mail
from .models import MainTradesBuyOrder, MainTradesSellOrder , MainTrades, ProTrades, Notification, VerifyMelliRequest , BankAccounts , VerifyBankAccountsRequest , Price , Staff, UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages ,Mainwalls, Forgetrequest, VerifyBankRequest
# Register your models here.

admin.site.register(UserInfo)
admin.site.register(Wallet)
admin.site.register(Currencies)
admin.site.register(Verify)
admin.site.register(BankCards)
admin.site.register(Transactions)
admin.site.register(Settings)
admin.site.register(Subjects)
admin.site.register(Tickets)
admin.site.register(Pages)
admin.site.register(Mainwalls)
admin.site.register(Forgetrequest)
admin.site.register(VerifyBankRequest)
admin.site.register(Staff)
admin.site.register(Price)
admin.site.register(VerifyMelliRequest)
admin.site.register(VerifyBankAccountsRequest)
admin.site.register(BankAccounts)
admin.site.register(Notification)
admin.site.register(MainTrades)
admin.site.register(ProTrades)
admin.site.register(MainTradesBuyOrder)
admin.site.register(MainTradesSellOrder)