from django import forms

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


class PromoterProfileForm(forms.Form):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    phone = forms.CharField(max_length=11, required=False)
    address = forms.CharField(max_length=150, required=False)
    bank_account_name = forms.CharField(max_length=150, required=False)
    bank_account_number = forms.CharField(max_length=10, required=False)
    bank_name = forms.ChoiceField(
        choices=BANK_CHOICES, label="(Select Bank)", required=False)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=150, required=False)
    message = forms.CharField(max_length=999999, required=True)
