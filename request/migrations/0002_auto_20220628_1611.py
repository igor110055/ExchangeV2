# Generated by Django 3.1.14 on 2022-06-28 16:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='depositrequest',
            name='payment_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='depositrequest',
            name='tx_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='withdrawrequest',
            name='payment_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='withdrawrequest',
            name='tx_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
