# Generated by Django 3.2.3 on 2021-05-26 09:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exchange', '0003_currencies_wallet'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankCards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='bank')),
                ('number', models.IntegerField()),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=300)),
                ('tel', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('telegram', models.CharField(max_length=300)),
                ('whatsapp', models.CharField(max_length=300)),
                ('instagram', models.CharField(max_length=300)),
                ('facebook', models.CharField(max_length=300)),
                ('logo', models.ImageField(null=True, upload_to='settings')),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('lastdate', models.DateField(default=django.utils.timezone.now)),
                ('act', models.IntegerField(default=0, null=True)),
                ('read', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=100)),
                ('aread', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Subject', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Verify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobileverify', models.BooleanField(default=False, null=True)),
                ('mobilecode', models.IntegerField(null=True)),
                ('emailverify', models.BooleanField(default=False, null=True)),
                ('emailcode', models.IntegerField(null=True)),
                ('melliverify', models.IntegerField(default=0, null=True)),
                ('bankverify', models.IntegerField(default=0, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verify', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='curid',
        ),
        migrations.AddField(
            model_name='wallet',
            name='currency',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='currency', to='exchange.currencies'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='mobile',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='VerifyMelliRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('melliimg', models.ImageField(null=True, upload_to='melli')),
                ('mellic', models.IntegerField(null=True)),
                ('action', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='melli', to=settings.AUTH_USER_MODEL)),
                ('verify', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exchange.verify')),
            ],
        ),
        migrations.CreateModel(
            name='VerifyBankRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bankimg', models.ImageField(null=True, upload_to='bank')),
                ('bankc', models.IntegerField(null=True)),
                ('action', models.BooleanField(default=False)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exchange.bankcards')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Bank', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('amount', models.FloatField()),
                ('act', models.IntegerField()),
                ('curid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to='exchange.currencies')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('text', models.CharField(max_length=1000)),
                ('pic', models.ImageField(null=True, upload_to='ticket')),
                ('subid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket', to='exchange.subjects')),
            ],
        ),
    ]
