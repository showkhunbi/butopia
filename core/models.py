from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from autoslug import AutoSlugField

# Create your models here.

BANK_CHOICES = (
    ('044', 'Access Bank'),
    ('063', 'Access Bank (Diamond)'),
    ('035A', 'ALAT by WEMA'),
    ('401', 'ASO Savings and Loans'),
    ('50931', 'Bowen Microfinance Bank'),
    ('50823', 'CEMCS Microfinance Bank'),
    ('023', 'Citibank Nigeria'),
    ('559', 'Coronation Merchant Bank'),
    ('050', 'Ecobank Nigeria'),
    ('562', 'Ekondo Microfinance Bank'),
    ('50126', 'Eyowo'),
    ('070', 'Fidelity Bank'),
    ('011', 'First Bank of Nigeria'),
    ('214', 'First City Monument Bank'),
    ('501', 'FSDH Merchant Bank Limited'),
    ('00103', 'Globus Bank'),
    ('058', 'Guaranty Trust Bank'),
    ('51251', 'Hackman Microfinance Bank'),
    ('50383', 'Hasal Microfinance Bank'),
    ('030', 'Heritage Bank'),
    ('51244', 'Ibile Microfinance Bank'),
    ('50457', 'Infinity MFB'),
    ('301', 'Jaiz Bank'),
    ('082', 'Keystone Bank'),
    ('50211', 'Kuda Bank'),
    ('90052', 'Lagos Building Investment Company Plc.'),
    ('565', 'One Finance'),
    ('999991', 'PalmPay'),
    ('526', 'Parallex Bank'),
    ('311', 'Parkway - ReadyCash'),
    ('999992', 'Paycom'),
    ('50746', 'Petra Mircofinance Bank Plc'),
    ('076', 'Polaris Bank'),
    ('101', 'Providus Bank'),
    ('125', 'Rubies MFB'),
    ('51310', 'Sparkle Microfinance Bank'),
    ('221', 'Stanbic IBTC Bank'),
    ('068', 'Standard Chartered Bank'),
    ('232', 'Sterling Bank'),
    ('100', 'Suntrust Bank'),
    ('302', 'TAJ Bank'),
    ('51211', 'TCF MFB'),
    ('102', 'Titan Bank'),
    ('032', 'Union Bank of Nigeria'),
    ('033', 'United Bank For Africa'),
    ('215', 'Unity Bank'),
    ('566', 'VFD Microfinance Bank Limited'),
    ('035', 'Wema Bank'),
    ('057', 'Zenith Bank'),
)


class Customer(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=11)
    number_of_devices = models.IntegerField(default=0)
    number_of_registered_devices = models.IntegerField(default=0)
    device = models.CharField(max_length=9999999, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name } {self.last_name}"


class Promoter(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField()
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    bank_account_name = models.CharField(max_length=150, blank=True, null=True)
    bank_account_number = models.CharField(
        max_length=10, blank=True, null=True)
    bank_name = models.CharField(
        choices=BANK_CHOICES, max_length=6, blank=True, null=True)
    bank_resolved = models.BooleanField(default=False)
    complete_profile = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='username')

    def __str__(self):
        return self.username

    def get_referral_url(self):
        return reverse("core:referrerPaymentView", kwargs={"slug": self.slug})


class Order(models.Model):
    customer = models.ForeignKey(
        "Customer", on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=20)
    reference = models.CharField(max_length=10)
    amount = models.IntegerField()
    paid_at = models.CharField(max_length=50)
    referrer = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.reference


class ReferrerOrder(models.Model):
    customer = models.ForeignKey(
        "Customer", on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, blank=True, null=True)
    successful_payment = models.BooleanField(default=False)
    promoter = models.ForeignKey(
        Promoter, on_delete=models.SET_NULL, blank=True, null=True)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.order.reference


class AccountInfo(models.Model):
    promoter = models.ForeignKey(
        "Promoter", on_delete=models.SET_NULL, blank=True, null=True)
    bank_name = models.CharField(max_length=50)
    bank_account_number = models.CharField(max_length=10)
    bank_account_name = models.CharField(max_length=150)
    recipient_code = models.CharField(max_length=100)

    def __str__(self):
        return self.bank_account_name


class TransferRequest(models.Model):
    promoter = models.ForeignKey(
        "Promoter", on_delete=models.SET_NULL, blank=True, null=True)
    bank_name = models.CharField(max_length=50)
    bank_account_number = models.CharField(max_length=10)
    bank_account_name = models.CharField(max_length=150)
    time = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    transfer_initialized = models.BooleanField(default=False)
    transfer_successful = models.BooleanField(default=False)

    def __str__(self):
        return self.bank_account_name


class TrialInstance(models.Model):
    device_id = models.CharField(max_length=50)
    trial_start_date = models.CharField(max_length=50)

    def __str__(self):
        return self.device_id


class FlexibleData(models.Model):
    key = models.CharField(max_length=99999)
    value = models.CharField(max_length=99999)

    def __str__(self):
        return self.key
