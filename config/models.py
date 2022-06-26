from django.db import models
from solo.models import SingletonModel


# Create your models here.
class WebsiteConfiguration(SingletonModel):
    fee  = models.CharField(max_length=100, verbose_name="Withdraw Fee in percents")
    api_name = models.CharField(max_length=255, verbose_name="API name", blank=True)
    secret_key = models.CharField(max_length=255, verbose_name="Secret key", blank=True)
    password_md5 = models.CharField(max_length=255, verbose_name="Password", blank=True)
