# Generated by Django 3.2.6 on 2021-10-12 16:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exchange', '0076_auto_20211003_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cp_withdraw',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 16, 26, 4, 267379, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='forgetrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 16, 26, 4, 274345, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintradesbuyorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 16, 26, 4, 277430, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintradessellorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 16, 26, 4, 278050, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 16, 26, 4, 275882, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='perpetualrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 16, 26, 4, 261491, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='protradesbuyorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 16, 26, 4, 278599, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='protradessellorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 16, 26, 4, 279291, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 16, 26, 4, 272537, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 16, 26, 4, 273096, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 10, 12, 16, 26, 4, 271164, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='buyrequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2021, 10, 12, 16, 26, 4, 260111, tzinfo=utc))),
                ('currency', models.CharField(max_length=20)),
                ('ramount', models.IntegerField()),
                ('camount', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buys', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]