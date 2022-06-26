# Generated by Django 3.1.14 on 2022-06-26 08:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0008_auto_20220626_0007'),
    ]

    operations = [
        migrations.AddField(
            model_name='currencies',
            name='active',
            field=models.BooleanField(blank=True, default=True, verbose_name='Show in website'),
        ),
        migrations.AddField(
            model_name='currencies',
            name='alfaname',
            field=models.CharField(blank=True, help_text='bitcoin, ethereum', max_length=50, verbose_name='AlfaCoin name'),
        ),
        migrations.AddField(
            model_name='currencies',
            name='symbol',
            field=models.CharField(blank=True, help_text='BTC, ETH ...', max_length=50, verbose_name='Symbol'),
        ),
        migrations.AlterField(
            model_name='buyapp',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 465156, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='buyoutrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 466140, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='buyrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 464830, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cp_withdraw',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 469282, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cpdepositrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 470975, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='exchangerequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 465728, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='forgetrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 474887, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='grid',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 480529, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintradesbuyorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 477881, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintradessellorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 478329, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 476848, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='perpetualrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 467181, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='profitlist',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 474133, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='protradesbuyorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 478666, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='protradessellorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 479014, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 463976, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='selloutrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 466558, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sellrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 465424, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='smsverified',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 463428)),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 473343, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 473682, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 472604, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 462951, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='otp',
            field=models.CharField(default='921d3zn29tjw5181', max_length=100),
        ),
        migrations.AlterField(
            model_name='withdrawrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 8, 17, 42, 470648, tzinfo=utc)),
        ),
    ]
