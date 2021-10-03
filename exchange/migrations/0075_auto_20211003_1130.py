# Generated by Django 3.2.6 on 2021-10-03 11:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0074_auto_20211003_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='pages',
            name='pic',
            field=models.ImageField(null=True, upload_to='pages'),
        ),
        migrations.AddField(
            model_name='pages',
            name='position',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cp_withdraw',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 3, 11, 30, 16, 121496, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='forgetrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 3, 11, 30, 16, 128931, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintradesbuyorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 3, 11, 30, 16, 132196, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintradessellorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 3, 11, 30, 16, 132715, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 3, 11, 30, 16, 130744, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='perpetualrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 3, 11, 30, 16, 116024, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='protradesbuyorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 3, 11, 30, 16, 133377, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='protradessellorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 3, 11, 30, 16, 133931, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 3, 11, 30, 16, 127287, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 3, 11, 30, 16, 127880, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 10, 3, 11, 30, 16, 126116, tzinfo=utc)),
        ),
    ]
