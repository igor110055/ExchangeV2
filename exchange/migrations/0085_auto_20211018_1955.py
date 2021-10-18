# Generated by Django 3.2.6 on 2021-10-18 19:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0084_auto_20211017_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='LevelFee',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('buy', models.FloatField()),
                ('sell', models.FloatField()),
                ('perpetual', models.FloatField()),
                ('margin', models.FloatField()),
                ('exchange', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SmsVerified',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20)),
                ('date', models.DateTimeField(default=datetime.datetime(2021, 10, 18, 19, 55, 52, 566036, tzinfo=utc))),
            ],
        ),
        migrations.RenameField(
            model_name='userinfo',
            old_name='is_smsverified',
            new_name='smsverify',
        ),
        migrations.AlterField(
            model_name='buyrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 18, 19, 55, 52, 568091, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cp_withdraw',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 18, 19, 55, 52, 574081, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='forgetrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 18, 19, 55, 52, 580789, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintradesbuyorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 18, 19, 55, 52, 583745, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintradessellorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 18, 19, 55, 52, 584325, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 18, 19, 55, 52, 582248, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='perpetualrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 18, 19, 55, 52, 569733, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='protradesbuyorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 18, 19, 55, 52, 584841, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='protradessellorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 18, 19, 55, 52, 585358, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 18, 19, 55, 52, 566760, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sellrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 18, 19, 55, 52, 568577, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 18, 19, 55, 52, 578985, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 18, 19, 55, 52, 579612, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 10, 18, 19, 55, 52, 577870, tzinfo=utc)),
        ),
    ]