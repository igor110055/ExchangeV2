# Generated by Django 3.1.14 on 2022-06-29 10:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0016_auto_20220628_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyapp',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 820658, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='buyoutrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 821688, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='buyrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 820232, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cp_withdraw',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 825133, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cpdepositrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 826964, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='exchangerequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 821313, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='forgetrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 831174, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='grid',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 837414, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintradesbuyorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 833918, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintradessellorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 834524, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 832195, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='perpetualrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 822889, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='profitlist',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 830439, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='protradesbuyorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 835149, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='protradessellorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 835570, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 819047, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='selloutrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 822089, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sellrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 820958, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='smsverified',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 818395)),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 829440, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 829899, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 828700, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 817526, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='otp',
            field=models.CharField(default='j7vag6a801wdqy68', max_length=100),
        ),
        migrations.AlterField(
            model_name='withdrawrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 10, 27, 7, 826599, tzinfo=utc)),
        ),
    ]