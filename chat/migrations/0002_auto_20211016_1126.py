# Generated by Django 3.2.6 on 2021-10-16 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatsessionmessage',
            name='aseen',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chatsessionmessage',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]
