# Generated by Django 3.1.3 on 2020-12-01 13:19

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=11)),
                ('number_of_devices', models.IntegerField(default=0)),
                ('number_of_registered_devices', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('reference', models.CharField(max_length=10)),
                ('amount', models.IntegerField()),
                ('paid_at', models.CharField(max_length=50)),
                ('referrer', models.CharField(blank=True, max_length=20, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Promoter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(blank=True, max_length=150, null=True)),
                ('last_name', models.CharField(blank=True, max_length=150, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=11, null=True)),
                ('address', models.CharField(blank=True, max_length=150, null=True)),
                ('bank_account_name', models.CharField(blank=True, max_length=150, null=True)),
                ('bank_account_number', models.CharField(blank=True, max_length=10, null=True)),
                ('bank_name', models.CharField(blank=True, choices=[('044', 'Access Bank'), ('063', 'Access Bank (Diamond)'), ('035A', 'ALAT by WEMA'), ('401', 'ASO Savings and Loans'), ('50931', 'Bowen Microfinance Bank'), ('50823', 'CEMCS Microfinance Bank'), ('023', 'Citibank Nigeria'), ('559', 'Coronation Merchant Bank'), ('050', 'Ecobank Nigeria'), ('562', 'Ekondo Microfinance Bank'), ('50126', 'Eyowo'), ('070', 'Fidelity Bank'), ('011', 'First Bank of Nigeria'), ('214', 'First City Monument Bank'), ('501', 'FSDH Merchant Bank Limited'), ('00103', 'Globus Bank'), ('058', 'Guaranty Trust Bank'), ('51251', 'Hackman Microfinance Bank'), ('50383', 'Hasal Microfinance Bank'), ('030', 'Heritage Bank'), ('51244', 'Ibile Microfinance Bank'), ('50457', 'Infinity MFB'), ('301', 'Jaiz Bank'), ('082', 'Keystone Bank'), ('50211', 'Kuda Bank'), ('90052', 'Lagos Building Investment Company Plc.'), ('565', 'One Finance'), ('999991', 'PalmPay'), ('526', 'Parallex Bank'), ('311', 'Parkway - ReadyCash'), ('999992', 'Paycom'), ('50746', 'Petra Mircofinance Bank Plc'), ('076', 'Polaris Bank'), ('101', 'Providus Bank'), ('125', 'Rubies MFB'), ('51310', 'Sparkle Microfinance Bank'), ('221', 'Stanbic IBTC Bank'), ('068', 'Standard Chartered Bank'), ('232', 'Sterling Bank'), ('100', 'Suntrust Bank'), ('302', 'TAJ Bank'), ('51211', 'TCF MFB'), ('102', 'Titan Bank'), ('032', 'Union Bank of Nigeria'), ('033', 'United Bank For Africa'), ('215', 'Unity Bank'), ('566', 'VFD Microfinance Bank Limited'), ('035', 'Wema Bank'), ('057', 'Zenith Bank')], max_length=6, null=True)),
                ('bank_resolved', models.BooleanField(default=False)),
                ('complete_profile', models.BooleanField(default=False)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='username')),
            ],
        ),
        migrations.CreateModel(
            name='TransferRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=50)),
                ('bank_account_number', models.CharField(max_length=10)),
                ('bank_account_name', models.CharField(max_length=150)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('amount', models.FloatField()),
                ('transfer_initialized', models.BooleanField(default=False)),
                ('transfer_successful', models.BooleanField(default=False)),
                ('promoter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.promoter')),
            ],
        ),
        migrations.CreateModel(
            name='ReferrerOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('successful_payment', models.BooleanField(default=False)),
                ('checked', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.customer')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.order')),
                ('promoter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.promoter')),
            ],
        ),
        migrations.CreateModel(
            name='AccountInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=50)),
                ('bank_account_number', models.CharField(max_length=10)),
                ('bank_account_name', models.CharField(max_length=150)),
                ('recipient_code', models.CharField(max_length=100)),
                ('promoter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.promoter')),
            ],
        ),
    ]