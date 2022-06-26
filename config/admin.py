from django.contrib import admin
from .models import WebsiteConfiguration

from solo.admin import SingletonModelAdmin
# Register your models here.
admin.site.register(WebsiteConfiguration, SingletonModelAdmin)