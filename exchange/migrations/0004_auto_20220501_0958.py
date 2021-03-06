# Generated by Django 3.0.14 on 2022-05-01 09:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0003_auto_20220430_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='grid',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 59, 12664, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='buyapp',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 58, 991656, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='buyoutrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 58, 992960, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='buyrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 58, 991177, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cp_withdraw',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 58, 997227, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cpdepositrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 58, 999299, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='exchangerequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 58, 992470, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='forgetrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 59, 6015, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintradesbuyorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 59, 8829, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintradessellorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 59, 9282, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 59, 7402, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='perpetualrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 58, 994435, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='profitlist',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 59, 4641, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='protradesbuyorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 59, 9937, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='protradessellorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 59, 10479, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 58, 989843, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='selloutrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 58, 993451, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sellrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 58, 992034, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='smsverified',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 58, 989229)),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 59, 3159, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 59, 3679, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 5, 1, 9, 58, 59, 1817, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 58, 988457, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='otp',
            field=models.CharField(default='kwafnx09m7db7w15', max_length=100),
        ),
        migrations.AlterField(
            model_name='withdrawrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 9, 58, 58, 998904, tzinfo=utc)),
        ),
    ]
