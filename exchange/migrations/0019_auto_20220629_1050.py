# Generated by Django 3.1.14 on 2022-06-29 10:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0018_auto_20220629_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyapp',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 324622, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='buyoutrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 325542, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='buyrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 324295, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cp_withdraw',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 328732, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cpdepositrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 330627, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='exchangerequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 325212, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='forgetrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 334836, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='grid',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 339508, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintradesbuyorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 336791, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintradessellorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 337130, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 335856, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='perpetualrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 326663, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='profitlist',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 334141, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='protradesbuyorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 337544, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='protradessellorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 337889, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 323350, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='selloutrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 325926, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sellrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 324903, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='smsverified',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 322936)),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 333258, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 333613, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 332448, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 322485, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='otp',
            field=models.CharField(default='yzj58mb1s15sv188', max_length=100),
        ),
        migrations.AlterField(
            model_name='withdrawrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 50, 25, 330245, tzinfo=utc)),
        ),
    ]
