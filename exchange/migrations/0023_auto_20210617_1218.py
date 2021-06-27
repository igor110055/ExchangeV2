# Generated by Django 3.2.3 on 2021-06-17 12:18

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exchange', '0022_auto_20210616_1059'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staff',
            old_name='User',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='forgetrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 17, 12, 18, 15, 917380)),
        ),
        migrations.AlterField(
            model_name='verifybankrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Banks', to=settings.AUTH_USER_MODEL),
        ),
    ]
