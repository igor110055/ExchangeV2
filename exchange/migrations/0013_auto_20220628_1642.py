# Generated by Django 3.1.14 on 2022-06-28 16:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0012_auto_20220628_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyapp',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 517609, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='buyoutrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 518661, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='buyrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 517221, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cp_withdraw',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 522015, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cpdepositrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 523877, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='exchangerequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 518221, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='forgetrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 527956, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='grid',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 533321, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintradesbuyorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 530685, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintradessellorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 531033, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 528982, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='perpetualrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 519797, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='profitlist',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 527094, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='protradesbuyorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 531406, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='protradessellorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 531748, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 516360, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='selloutrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 519056, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sellrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 517881, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='smsverified',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 515934)),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 526324, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 526676, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 525606, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 515393, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='otp',
            field=models.CharField(default='6n1w8ahzs31nxy47', max_length=100),
        ),
        migrations.AlterField(
            model_name='withdrawrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 42, 3, 523490, tzinfo=utc)),
        ),
    ]