# Generated by Django 3.2.3 on 2021-07-07 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0029_auto_20210706_1410'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verifymellirequest',
            name='verify',
        ),
    ]
