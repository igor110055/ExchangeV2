# Generated by Django 3.0.14 on 2022-04-03 06:58

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import jsonfield.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=16, null=True)),
                ('shebac', models.CharField(max_length=50, null=True)),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BottomSticker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.ImageField(null=True, upload_to='docs')),
                ('text', models.CharField(max_length=16, null=True)),
                ('img', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Cp_Currencies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=100, null=True)),
                ('chain', models.CharField(max_length=100, null=True)),
                ('can_deposit', models.CharField(max_length=100, null=True)),
                ('can_withdraw', models.CharField(max_length=100, null=True)),
                ('deposit_least_amount', models.CharField(max_length=100, null=True)),
                ('withdraw_least_amount', models.CharField(max_length=100, null=True)),
                ('withdraw_tx_fee', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Currencies',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name=' ?????? ??????')),
                ('brand', models.CharField(max_length=100, null=True, verbose_name=' ???????? ??????')),
                ('pic', models.ImageField(null=True, upload_to='cur')),
            ],
            options={
                'verbose_name': ' ?????? ',
                'verbose_name_plural': ' ?????? ????',
            },
        ),
        migrations.CreateModel(
            name='Forgetrequest',
            fields=[
                ('email', models.CharField(max_length=200, null=True)),
                ('key', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 604233, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='General',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('mobile', models.CharField(max_length=255)),
                ('whatsapp', models.CharField(max_length=255)),
                ('telegram', models.CharField(max_length=255)),
                ('instagram', models.CharField(max_length=255)),
                ('telephone', models.CharField(max_length=255)),
                ('rule', models.CharField(max_length=1000000, null=True)),
                ('logo', models.ImageField(null=True, upload_to='general')),
                ('USDTpercent', models.FloatField(null=True)),
                ('USDTpercent2', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Indexprice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', jsonfield.fields.JSONField(default=dict)),
                ('PriceHistory', jsonfield.fields.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='LevelFee',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('buy', models.FloatField(default=0)),
                ('sell', models.FloatField(default=0)),
                ('perpetual', models.FloatField(default=0)),
                ('margin', models.FloatField(default=0)),
                ('exchange', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Leverage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=100)),
                ('leverage', models.IntegerField(default=0)),
                ('buymin', models.FloatField(null=True)),
                ('buymax', models.FloatField(null=True)),
                ('sellmin', models.FloatField(null=True)),
                ('sellmax', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MainTrades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name=' ?????? ??????')),
                ('brand', models.CharField(max_length=100, null=True, verbose_name=' ???????? ??????')),
                ('bcurrency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buycurrency', to='exchange.Currencies')),
                ('scurrency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sellcurrency', to='exchange.Currencies')),
            ],
        ),
        migrations.CreateModel(
            name='mobilecodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=15)),
                ('code', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.ImageField(null=True, upload_to='docs')),
                ('text', models.CharField(max_length=16, null=True)),
                ('img', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('pic', models.ImageField(null=True, upload_to='pages')),
                ('title', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=1000000)),
                ('minitext', models.CharField(default='', max_length=1000, null=True)),
                ('position', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.ImageField(null=True, upload_to='docs')),
                ('text', models.CharField(max_length=16, null=True)),
                ('img', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rial', models.FloatField(default=1)),
                ('btc', models.FloatField(default=0)),
                ('eth', models.FloatField(default=0)),
                ('trx', models.FloatField(default=0)),
                ('usdt', models.FloatField(default=0)),
                ('doge', models.FloatField(default=0)),
                ('usd', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PriceHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rial', models.FloatField(default=1)),
                ('btc', models.FloatField(default=0)),
                ('eth', models.FloatField(default=0)),
                ('trx', models.FloatField(default=0)),
                ('usdt', models.FloatField(default=0)),
                ('doge', models.FloatField(default=0)),
                ('usd', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ProTrades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name=' ?????? ??????')),
                ('brand', models.CharField(max_length=100, null=True, verbose_name=' ???????? ??????')),
                ('bcurrency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='probuycurrency', to='exchange.Currencies')),
                ('scurrency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prosellcurrency', to='exchange.Currencies')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 592008, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
            name='SmsVerified',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20)),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 591497))),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 602711, tzinfo=utc))),
                ('act', models.IntegerField(default=0, null=True)),
                ('read', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=100)),
                ('aread', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Subject', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TopSticker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.ImageField(null=True, upload_to='docs')),
                ('text', models.CharField(max_length=16, null=True)),
                ('img', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='WithdrawRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 599614, tzinfo=utc))),
                ('amount', models.BigIntegerField()),
                ('act', models.IntegerField(default=0)),
                ('bankaccount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account', to='exchange.BankAccounts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdraws', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
                ('address', models.CharField(blank=True, max_length=1000, null=True)),
                ('key', models.CharField(blank=True, max_length=1000, null=True)),
                ('accid', models.CharField(blank=True, max_length=100, null=True)),
                ('currency', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='exchange.Currencies')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': ' ?????? ?????? ',
                'verbose_name_plural': ' ?????? ?????? ????',
            },
        ),
        migrations.CreateModel(
            name='VerifyMelliRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('melliimg', models.ImageField(null=True, upload_to='melli')),
                ('mellic', models.CharField(max_length=16, null=True)),
                ('action', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='melli', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VerifyBankRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bankc', models.CharField(max_length=16, null=True)),
                ('action', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Banks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VerifyBankAccountsRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bankc', models.CharField(blank=True, max_length=16, null=True)),
                ('shebac', models.CharField(max_length=50, null=True)),
                ('action', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BanksAccounts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VerifyAcceptRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acceptimg', models.ImageField(upload_to='accept')),
                ('action', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accept', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Verify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobilev', models.BooleanField(default=False, null=True)),
                ('mobilec', models.IntegerField(default=0, null=True)),
                ('emailv', models.BooleanField(default=False, null=True)),
                ('emailc', models.IntegerField(default=0, null=True)),
                ('acceptv', models.BooleanField(default=False, null=True)),
                ('melliv', models.BooleanField(default=False, null=True)),
                ('bankv', models.BooleanField(default=False, null=True)),
                ('accountv', models.BooleanField(default=False, null=True)),
                ('idv', models.BooleanField(default=False, null=True)),
                ('rulev', models.BooleanField(default=False, null=True)),
                ('coinv', models.BooleanField(default=False, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('mobile', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=500, null=True)),
                ('post', models.CharField(max_length=10, null=True)),
                ('level', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('is_verify', models.BooleanField(default=False)),
                ('smsverify', models.BooleanField(default=False)),
                ('googleverify', models.BooleanField(default=False)),
                ('emailverify', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('last_visit', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 590931, tzinfo=utc))),
                ('complete', models.BooleanField(default=False)),
                ('otp', models.CharField(default='w1j1ztw2rf42m692', max_length=100)),
                ('referalid', models.UUIDField(default=uuid.uuid4)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userinfo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 601934, tzinfo=utc))),
                ('amount', models.FloatField()),
                ('act', models.IntegerField()),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to='exchange.Currencies')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='transactionid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transid', models.UUIDField(editable=False)),
                ('amount', models.BigIntegerField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactionid', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 603077, tzinfo=utc))),
                ('text', models.CharField(max_length=1000)),
                ('pic', models.ImageField(null=True, upload_to='ticket')),
                ('subid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket', to='exchange.Subjects')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='harchi', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staffs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='sellrequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 593833, tzinfo=utc))),
                ('currency', models.CharField(max_length=20)),
                ('ramount', models.FloatField()),
                ('camount', models.FloatField()),
                ('act', models.IntegerField(default=2)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sells', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='selloutrequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 594980, tzinfo=utc))),
                ('currency', models.CharField(max_length=20)),
                ('hash', models.CharField(max_length=200)),
                ('ramount', models.FloatField()),
                ('rramount', models.FloatField(null=True)),
                ('camount', models.FloatField()),
                ('act', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sellout', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Referal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inviter', models.IntegerField()),
                ('inviting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProTradesSellOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('price', models.FloatField()),
                ('start', models.FloatField(null=True)),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 607305, tzinfo=utc))),
                ('trade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sellorders', to='exchange.ProTrades')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='protradesellorders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProTradesBuyOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('price', models.FloatField()),
                ('start', models.FloatField(null=True)),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 606908, tzinfo=utc))),
                ('trade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyorders', to='exchange.ProTrades')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='protradebuyorders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfitList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 603564, tzinfo=utc))),
                ('amount', models.FloatField()),
                ('currency', models.CharField(max_length=10)),
                ('operation', models.CharField(max_length=200)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profit', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PerpetualRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 595730, tzinfo=utc))),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Perpetualreq', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Perpetual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('secretkey', models.CharField(max_length=255)),
                ('apikey', models.CharField(max_length=255)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Perpetual', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=300)),
                ('seen', models.BooleanField(default=False)),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 605182, tzinfo=utc))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MainTradesSellOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('price', models.FloatField()),
                ('start', models.FloatField(null=True)),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 606558, tzinfo=utc))),
                ('trade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sellorders', to='exchange.MainTrades')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintradesellorders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MainTradesBuyOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('price', models.FloatField()),
                ('start', models.FloatField(null=True)),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 606223, tzinfo=utc))),
                ('trade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyorders', to='exchange.MainTrades')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintradebuyorders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='exchangerequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 594195, tzinfo=utc))),
                ('currency', models.CharField(max_length=20)),
                ('currency2', models.CharField(max_length=20)),
                ('camount', models.FloatField()),
                ('camount2', models.FloatField()),
                ('act', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchanges', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CpDepositRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=1000)),
                ('currency', models.CharField(max_length=10)),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 599992, tzinfo=utc))),
                ('amount', models.BigIntegerField()),
                ('act', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cpdeposits', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cp_Withdraw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 598080, tzinfo=utc))),
                ('chain', models.CharField(max_length=10)),
                ('amount', models.FloatField()),
                ('address', models.CharField(blank=True, max_length=1000, null=True)),
                ('rejected', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('currency', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='exchange.Cp_Currencies')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cp_Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=1000, null=True)),
                ('currency', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='exchange.Cp_Currencies')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='buyrequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 593063, tzinfo=utc))),
                ('currency', models.CharField(max_length=20)),
                ('ramount', models.BigIntegerField()),
                ('rramount', models.FloatField(null=True)),
                ('camount', models.FloatField()),
                ('act', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buys', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='buyoutrequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 594550, tzinfo=utc))),
                ('currency', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=200)),
                ('ramount', models.BigIntegerField()),
                ('rramount', models.FloatField(null=True)),
                ('camount', models.FloatField()),
                ('act', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyout', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='buyapp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 4, 3, 6, 58, 21, 593450, tzinfo=utc))),
                ('type', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyapps', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BankCards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=16, null=True)),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
