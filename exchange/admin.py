from django.contrib import admin
from .models import Staff, UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages ,Mainwalls, Forgetrequest, VerifyBankRequest
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