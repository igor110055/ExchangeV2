from django.db import models
from io import BytesIO
from PIL import Image
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from django.core.files import File
from django.utils.translation import deactivate
from jsonfield import JSONField
from datetime import datetime    
import django
from sarafi.settings import ROOT

class UserInfo(models.Model):
    user = models.ForeignKey(User , related_name='userinfo', on_delete=models.CASCADE)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    mobile = models.CharField(max_length=10,)
    email = models.EmailField()
    level = models.IntegerField(default= 0)
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
    address = models.CharField(max_length=1000 , null = True)
    key = models.CharField(max_length=1000 , null = True)
    class Meta:
        verbose_name = ' کیف پول '
        verbose_name_plural = ' کیف پول ها'



class Verify(models.Model):
    user = models.ForeignKey(User , related_name='verify' , on_delete=models.CASCADE)
    mobileverify = models.BooleanField(default = False , null = True)
    mobilecode = models.IntegerField( null = True,default=0)
    emailverify = models.BooleanField(default = False , null = True)
    emailcode = models.IntegerField( null = True ,default=0)
    melliverify = models.BooleanField(default = False , null = True)
    bankverify = models.BooleanField(default = False , null = True)
    class meta:
        verbose_name = ' تاییدیه '
        verbose_name_plural = ' تاییدیه ها'


class BankCards(models.Model):
    user =  models.ForeignKey(User , related_name='cards' , on_delete=models.CASCADE)
    image = models.ImageField(upload_to='bank')
    number = models.IntegerField()
    status = models.BooleanField(default=False)
    class meta:
        verbose_name = ' کارت بانک '
        verbose_name_plural = ' کارت های بانک'


class VerifyMelliRequest(models.Model):
    user = models.ForeignKey(User , related_name='melli' , on_delete=models.CASCADE)
    verify = models.ForeignKey(Verify , on_delete=models.CASCADE)
    melliimg = models.ImageField(upload_to='melli' , null = True)
    mellic = models.IntegerField( null = True)
    action = models.BooleanField(default = False)
    class meta:
        verbose_name = ' درخواست تایید کارت ملی '
        verbose_name_plural = ' درخواست های تایید کارت ملی '

class VerifyBankRequest(models.Model):
    user = models.ForeignKey(User , related_name='Banks' , on_delete=models.CASCADE)
    bankimg = models.ImageField(upload_to='bank' , null = True)
    bankc = models.IntegerField( null = True)
    action = models.BooleanField(default = False)
    class meta:
        verbose_name = ' درخواست تایید کارت بانکی '
        verbose_name_plural = ' درخواست های تایید کارت بانکی '
    def get_image(self):
        return f'{ROOT}/media/{self.bankimg}/'
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
    date = models.DateField(default=timezone.now) 
    lastdate = models.DateField(default=timezone.now)
    user = models.ForeignKey(User , related_name='Subject' , on_delete=models.CASCADE)
    act = models.IntegerField(null=True , default = 0)
    read = models.BooleanField(default = True)
    title = models.CharField(max_length = 100)
    aread = models.BooleanField(default = False)
    class meta:
        verbose_name = 'سر تیتر تیکت'
        verbose_name_plural = ' سرتیتر های تیکت '
    
class Tickets(models.Model):
    date = models.DateField(default=timezone.now) 
    subid = models.ForeignKey(Subjects , related_name='ticket' , on_delete=models.CASCADE)
    text = models.CharField(max_length = 1000)
    pic = models.ImageField(upload_to='ticket' , null = True)
    class meta:
        verbose_name = ' تیکت '
        verbose_name_plural = 'تیکت ها'


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