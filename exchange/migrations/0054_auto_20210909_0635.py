# Generated by Django 3.2.6 on 2021-09-09 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0053_auto_20210908_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='leverage',
            name='buymax',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='leverage',
            name='buymin',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='leverage',
            name='sellmax',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='leverage',
            name='sellmin',
            field=models.FloatField(null=True),
        ),
    ]