# Generated by Django 3.1.14 on 2022-06-25 23:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0005_auto_20220507_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyapp',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 547738, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='buyoutrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 548787, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='buyrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 547386, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cp_withdraw',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 551959, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cpdepositrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 553761, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='exchangerequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 548438, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='forgetrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 557717, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='grid',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 563486, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintradesbuyorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 560774, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintradessellorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 561157, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 558999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='perpetualrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 549882, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='profitlist',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 556980, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='protradesbuyorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 561516, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='protradessellorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 561866, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 546473, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='selloutrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 549189, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sellrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 548071, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='smsverified',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 545989)),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 556196, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 556560, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 555376, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 545304, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='otp',
            field=models.CharField(default='paayh8x5ct02q279', max_length=100),
        ),
        migrations.AlterField(
            model_name='withdrawrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 23, 49, 27, 553357, tzinfo=utc)),
        ),
    ]
