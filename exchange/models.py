from typing import Text
from django.db import models
from io import BytesIO
from PIL import Image
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from django.core.files import File
from django.utils.translation import deactivate
from jsonfield import JSONField
from datetime import date, datetime    
import django
from sarafi.settings import ROOT
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from django.utils.timezone import utc

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )

class UserInfo(models.Model):
    user = models.OneToOneField(User , related_name='userinfo', on_delete=models.CASCADE)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    mobile = models.CharField(max_length=10,)
    email = models.EmailField()
    level = models.IntegerField(default= 0)
    is_active = models.BooleanField(default=True)
    is_verify = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    class meta:
        ordering = ('-date_joined',)
        verbose_name = ' کاربر '
        verbose_name_plural = ' کاربر ها'
        
    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return f'/{self.username}/'

class Staff(models.Model):
    user = models.ForeignKey(User , related_name='staffs' , on_delete=models.CASCADE)
    level = models.IntegerField()

class Currencies(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100 ,verbose_name=" نام ارز")
    brand = models.CharField(max_length=100 ,null=True,verbose_name=" نماد ارز")
    pic = models.ImageField(upload_to='cur' , null = True)
    key = models.CharField(max_length=1000, null=True)
    class Meta:
        verbose_name = ' ارز '
        verbose_name_plural = ' ارز ها'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'currencies/{self.name}/'
    def get_image(self):
        return f'{ROOT}/media/{self.pic}/'

class Wallet(models.Model):
    user = models.ForeignKey(User , related_name='wallet' , on_delete=models.CASCADE)
    currency = models.ForeignKey(Currencies , related_name='currency', on_delete=models.CASCADE ,default=0)
    amount = models.FloatField(default=0)
    address = models.CharField(max_length=1000 , null = True, blank=True)
    key = models.CharField(max_length=1000 , null = True ,blank=True)
    class Meta:
        verbose_name = ' کیف پول '
        verbose_name_plural = ' کیف پول ها'



class Verify(models.Model):
    user = models.ForeignKey(User , related_name='verify' , on_delete=models.CASCADE)
    mobilev = models.BooleanField(default = False , null = True)
    mobilec = models.IntegerField( null = True,default=0)
    emailv = models.BooleanField(default = False , null = True)
    emailc = models.IntegerField( null = True ,default=0)
    melliv = models.BooleanField(default = False , null = True)
    bankv = models.BooleanField(default = False , null = True)
    class meta:
        verbose_name = ' تاییدیه '
        verbose_name_plural = ' تاییدیه ها'


class BankCards(models.Model):
    user =  models.ForeignKey(User , related_name='cards' , on_delete=models.CASCADE)
    image = models.ImageField(upload_to='bank')
    number = models.BigIntegerField()
    status = models.BooleanField(default=False)
    class meta:
        verbose_name = ' کارت بانک '
        verbose_name_plural = ' کارت های بانک'

class BankAccounts(models.Model):
    user =  models.ForeignKey(User , related_name='accounts' , on_delete=models.CASCADE)
    number = models.BigIntegerField()
    status = models.BooleanField(default=False)
    class meta:
        verbose_name = ' حساب بانکی '
        verbose_name_plural = ' حساب های بانک'

class VerifyMelliRequest(models.Model):
    user = models.ForeignKey(User , related_name='melli' , on_delete=models.CASCADE)
    melliimg = models.ImageField(upload_to='melli' , null = True)
    mellic = models.BigIntegerField( null = True)
    action = models.BooleanField(default = False)
    class meta:
        verbose_name = ' درخواست تایید کارت ملی '
        verbose_name_plural = ' درخواست های تایید کارت ملی '
    def get_image(self):
        return f'{ROOT}/media/{self.melliimg}/'
    def get_user(self):
        return f'{self.user.username}'

class VerifyBankRequest(models.Model):
    user = models.ForeignKey(User , related_name='Banks' , on_delete=models.CASCADE)
    bankimg = models.ImageField(upload_to='bank' , null = True)
    bankc = models.BigIntegerField( null = True)
    action = models.BooleanField(default = False)
    class meta:
        verbose_name = ' درخواست تایید کارت بانکی '
        verbose_name_plural = ' درخواست های تایید کارت بانکی '
    def get_image(self):
        return f'{ROOT}/media/{self.bankimg}/'
    def get_user(self):
        return f'{self.user.username}'

class VerifyBankAccountsRequest(models.Model):
    user = models.ForeignKey(User , related_name='BanksAccounts' , on_delete=models.CASCADE)
    bankc = models.BigIntegerField( null = True)
    action = models.BooleanField(default = False)
    class meta:
        verbose_name = ' درخواست تایید حساب بانکی '
        verbose_name_plural = ' درخواست های تایید حساب بانکی '
    def get_user(self):
        return f'{self.user.username}'

class Transactions(models.Model):
    date = models.DateField(default=timezone.now) 
    amount = models.FloatField()
    user = models.ForeignKey(User , related_name='transaction' , on_delete=models.CASCADE)
    currency = models.ForeignKey(Currencies , related_name='transaction' , on_delete=models.CASCADE)
    act = models.IntegerField()
    class meta:
        verbose_name = ' تراکنش  '
        verbose_name_plural = 'تراکنش ها '

class Settings(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    tel = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    telegram = models.CharField(max_length = 300)
    whatsapp = models.CharField(max_length = 300)
    instagram = models.CharField(max_length = 300)
    facebook = models.CharField(max_length = 300)
    logo = models.ImageField(upload_to='settings' , null=True)
    class meta:
        verbose_name = 'تنظیمات'


class Subjects(models.Model):
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User , related_name='Subject' , on_delete=models.CASCADE)
    act = models.IntegerField(null=True , default = 0)
    read = models.BooleanField(default = True)
    title = models.CharField(max_length = 100)
    aread = models.BooleanField(default = False)
    class meta:
        verbose_name = 'سر تیتر تیکت'
        verbose_name_plural = ' سرتیتر های تیکت '
    def get_lastticket(self):
        return self.ticket.all().order_by('-date').first().text

    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now() - self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes
    
class Tickets(models.Model):
    date = models.DateTimeField(default=timezone.now)
    subid = models.ForeignKey(Subjects , related_name='ticket' , on_delete=models.CASCADE)
    text = models.CharField(max_length = 1000)
    pic = models.ImageField(upload_to='ticket' , null = True)
    class meta:
        verbose_name = ' تیکت '
        verbose_name_plural = 'تیکت ها'

    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now() - self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes 

    def get_title(self):
        return self.subid.title
    def get_user(self):
        return self.subid.user.username


class Pages(models.Model):
    name = models.CharField(max_length = 100)
    title = models.CharField(max_length = 100)
    text = models.CharField(max_length = 10000)
    class meta:
        verbose_name = ' صفحه '
        verbose_name_plural = 'صفحات '

class Mainwalls(models.Model):
    name = models.CharField(max_length=100)
    currency = models.ForeignKey(Currencies , related_name='mainwalls' , on_delete=models.CASCADE, null=True)
    wall = JSONField()

class Forgetrequest(models.Model):
    email = models.CharField(max_length=200,null=True)
    key = models.UUIDField(max_length=100, primary_key=True, default=uuid.uuid4)
    date = models.DateTimeField(default=django.utils.timezone.now)

class Price(models.Model):
    rial = models.FloatField(default=1)
    btc = models.FloatField(default=0)
    eth = models.FloatField(default=0)
    trx = models.FloatField(default=0)
    usdt = models.FloatField(default=0)
    doge = models.FloatField(default=0)
    usd = models.FloatField(default=0)

class Notification(models.Model):
    user = models.ForeignKey(User , related_name='notifications' , on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=300)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)
    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now() - self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes 

class MainTrades(models.Model):
    name = models.CharField(max_length=100 ,verbose_name=" نام ارز")
    brand = models.CharField(max_length=100 ,null=True,verbose_name=" نماد ارز")
    scurrency = models.ForeignKey(Currencies , related_name='sellcurrency', on_delete=models.CASCADE , null=True)
    bcurrency = models.ForeignKey(Currencies , related_name='buycurrency' , on_delete=models.CASCADE , null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'{ROOT}/trades/{self.name}/'
    
    def get_bname(self):
        return self.bcurrency.name
    def get_sname(self):
        return self.scurrency.name


class ProTrades(models.Model):
    name = models.CharField(max_length=100 ,verbose_name=" نام ارز")
    brand = models.CharField(max_length=100 ,null=True,verbose_name=" نماد ارز")
    scurrency = models.ForeignKey(Currencies , related_name='prosellcurrency', on_delete=models.CASCADE , null=True)
    bcurrency = models.ForeignKey(Currencies , related_name='probuycurrency' , on_delete=models.CASCADE , null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'{ROOT}/trades/{self.name}/'

class MainTradesBuyOrder(models.Model):
    trade = models.ForeignKey(MainTrades, related_name='buyorders' , on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='maintradebuyorders' , on_delete=models.CASCADE)
    amount = models.FloatField()
    price = models.FloatField()
    start = models.FloatField(null=True)
    date = models.DateTimeField(default=timezone.now)
    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now() - self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes 



    def get_brand(self):
        return self.trade.bcurrency.brand

class MainTradesSellOrder(models.Model):
    trade = models.ForeignKey(MainTrades, related_name='sellorders' , on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='maintradesellorders' , on_delete=models.CASCADE)
    amount = models.FloatField()
    price = models.FloatField()
    start = models.FloatField(null=True)
    date = models.DateTimeField(default=timezone.now)
    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now() - self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes 


    def get_brand(self):
        return self.trade.bcurrency.brand
class ProTradesBuyOrder(models.Model):
    trade = models.ForeignKey(ProTrades, related_name='buyorders' , on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='protradebuyorders' , on_delete=models.CASCADE)
    amount = models.FloatField()
    price = models.FloatField()
    start = models.FloatField(null=True)
    date = models.DateTimeField(default=timezone.now)
    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now() - self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes 

    def get_brand(self):
        return self.trade.bcurrency.brand
class ProTradesSellOrder(models.Model):
    trade = models.ForeignKey(ProTrades, related_name='sellorders' , on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='protradesellorders' , on_delete=models.CASCADE)
    amount = models.FloatField()
    price = models.FloatField()
    start = models.FloatField(null=True)
    date = models.DateTimeField(default=timezone.now)
    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now() - self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes 

    def get_brand(self):
        return self.trade.bcurrency.brand