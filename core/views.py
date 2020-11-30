
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils.html import strip_tags
from .forms import PromoterProfileForm, ContactForm
from .models import Customer, Order, Promoter, ReferrerOrder, AccountInfo, TransferRequest, FlexibleData,  BANK_CHOICES

import requests
import json
from twilio.rest import Client


class HomeView(View):
    def get(self, request):
        context = {

        }
        return render(request, "buttons.html", context)


class PaymentView(View):
    def get(self, *args, **kwargs):
        context = {

        }
        if self.request.GET:
            email = self.request.GET["email"]
            context.update({"email": email})
        return render(self.request, "form.html", context)


class PortfolioView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "portfolio.html")


class ContactView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "contact.html")

    def post(self, *args, **kwargs):
        contact_form = ContactForm(self.request.POST or None)
        if contact_form.is_valid():
            name = contact_form.cleaned_data.get("name")
            if not name:
                name = "Anonymous"
            email = contact_form.cleaned_data.get("email")
            subject = contact_form.cleaned_data.get("subject")
            message = "Message from: " + name + "\n" + "Email: " + email + "\n\n" + \
                contact_form.cleaned_data.get("message")

            email_from = "contactForm@butopia.com.ng"
            recipient_list = ['butopia3+contactform@gmail.com',
                              "maximusjshokes+contactform@gmail.com", ]
            try:
                send_mail(subject, message, email_from, recipient_list)
                messages.success(
                    self.request, "Contact form successfully sent")
            except:
                messages.error(
                    self.request, "some kind of Error occured sending Email, try again")

            return redirect('core:contact')


def referrer_payment_view(request, slug):
    promoter = get_object_or_404(Promoter, slug=slug)
    referrer = promoter.username
    context = {
        "referrer": referrer
    }
    return render(request, "form.html", context)


def verify_transaction(request):
    reference = request.GET.get("reference")

    url = "https://api.paystack.co/transaction/verify/" + reference

    payload = {}
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    try:
        if response["data"]["status"] == "success":
            customer_qs = Customer.objects.filter(
                email=response["data"]["customer"]["email"])
            if customer_qs.exists():
                customer = Customer.objects.get(
                    email=response["data"]["customer"]["email"])
                customer.number_of_devices += 1
                customer.save()
                messages.success(
                    request, "Number of allowable devices increased by 1.")
            else:
                customer = Customer()
                customer.email = response["data"]["customer"]["email"]
                customer.first_name = response["data"]["metadata"]["first_name"]
                customer.last_name = response["data"]["metadata"]["last_name"]
                customer.phone_number = response["data"]["metadata"]["phone"]
                customer.number_of_devices += 1
                customer.save()

            order = Order()
            order.customer = customer
            order.status = response["data"]["status"]
            order.reference = response["data"]["reference"]
            order.amount = response["data"]["amount"] / 100
            order.paid_at = response["data"]["paid_at"]
            order.referrer = response["data"]["metadata"]["referrer_id"]
            order.save()

            if order.referrer != "":
                try:
                    promoter = Promoter.objects.get(username=order.referrer)
                    referrerOrder = ReferrerOrder()
                    referrerOrder.customer = customer
                    referrerOrder.order = order
                    if order.status == "success":
                        referrerOrder.successful_payment = True
                    referrerOrder.promoter = promoter
                    referrerOrder.save()
                except:
                    a = 2

            messages.success(
                request, "Payment Successful. Thank you for purchasing")

            try:
                subject_1 = "Successful Payment"
                # html_message = render_to_string(
                #    "emails/thank_you_for_purchasing.html", context={"customer": customer})
                html_message = f"""
                <h2>Hello {customer.first_name} </h2>
                <p>Thank you for purchasing the full version of FUNAAB Post UTME Past Questions
                    and Detailed solutions manual. Your payment has been successfully confirmed
                    and your email address has been registered. Don't know what to do?</p>
                <h4>Next Steps? Re-Enter your Email</h4>
                <p>It is as simple as that. Return to the FUNAAB Post
                    UTME Past Questions and answers app, click register
                    full version and enter your this email address which
                    has been confirmed for payment and you will be
                    automatically registered for full access. Don't have
                    the app, download <a href=https://butopia.com.ng/download>here</a>.</p>
                """
                plain_message = strip_tags(html_message)
                from_email = settings.DEFAULT_FROM_EMAIL
                to = customer.email
                send_mail(subject_1, plain_message,
                          from_email, [to], html_message=html_message)
                subject_2 = "Become a Promoter"
                # html_message_2 = render_to_string(
                #     "emails/become_a_promoter.html", context={"customer": customer})
                html_message_2 = f"""
                <h2>Hello {customer.first_name} </h2>
                <p>You can Earn back your money and more by joining B-Utopia League of
                    Promoters. Invite and Earn N200 intantly on each invited subscriber to buy
                    the FUNAAB Post UTME Past Questions and Detailed Solutions Manual.</p>
                <p><a href="https://butopia.com.ng/accounts/dashboard">Get Started</a></p>
                """
                plain_message_2 = strip_tags(html_message_2)
                send_mail(subject_2, plain_message_2,
                          from_email, [to], html_message=html_message_2)

            except Exception as e:
                print(e)
                messages.error(request, "Error sending mail")
        else:
            messages.error(request, "Unsuccessful Payment")
    except:
        messages.error(
            request, "Error occured while verifying your payment. If you have been charged, contact admin")

    return redirect("core:paymentview")


class PromoterProfileView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        form = PromoterProfileForm()
        user_info = {
            "username": self.request.user.username,
            "email": self.request.user.email,
        }
        context = {
            "form": form,
            "user_info": user_info,
        }
        try:
            promoter = Promoter.objects.get(
                username=self.request.user.username)
            context.update({"promoter": promoter})

        except:
            a = 1
        return render(self.request, "account/profile.html", context)

    def post(self, *args, **kwargs):
        form = PromoterProfileForm(self.request.POST or None)
        try:
            promoter = Promoter.objects.get(
                username=self.request.user.username)

            if form.is_valid():

                first_name = form.cleaned_data.get("first_name")
                last_name = form.cleaned_data.get("last_name")
                phone_number = form.cleaned_data.get("phone")
                address = form.cleaned_data.get("address")
                bank_account_name = form.cleaned_data.get("bank_account_name")
                bank_account_number = form.cleaned_data.get(
                    "bank_account_number")
                bank_name = form.cleaned_data.get("bank_name")

                promoter.first_name = first_name
                promoter.last_name = last_name
                promoter.phone_number = phone_number
                promoter.address = address
                promoter.bank_name = bank_name
                promoter.bank_account_name = bank_account_name
                promoter.bank_account_number = bank_account_number
                promoter.save()

                if promoter.bank_name and promoter.bank_account_number and promoter.bank_account_number:
                    url = f"https://api.paystack.co/bank/resolve?account_number={promoter.bank_account_number}&bank_code={promoter.bank_name}"

                    payload = {}
                    headers = {
                        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
                    }
                    response = requests.request(
                        "GET", url, headers=headers, data=payload)
                    response = response.json()
                    if response["message"] == "Account number resolved":
                        promoter.bank_account_name = response["data"]["account_name"]
                        promoter.bank_resolved = True
                        messages.success(self.request, "Bank Account Resolved")
                    else:
                        promoter.bank_resolved = False
                        messages.warning(
                            self.request, "Bank Information not resolved, Check and try again")
                else:
                    promoter.bank_resolved = False
                promoter.save()

                messages.success(self.request, "Profile Successfully updated")

                if (promoter.username and promoter.email and promoter.first_name and promoter.last_name and promoter.phone_number and promoter.address and promoter.bank_name and promoter.bank_account_name and promoter.bank_account_number and promoter.bank_resolved):
                    promoter.complete_profile = True
                    messages.success(
                        self.request, "Profile Successfully completed")

                else:
                    promoter.complete_profile = False
                promoter.save()
        except ObjectDoesNotExist:

            if form.is_valid():

                first_name = form.cleaned_data.get("first_name")
                last_name = form.cleaned_data.get("last_name")
                phone_number = form.cleaned_data.get("phone")
                address = form.cleaned_data.get("address")
                bank_account_name = form.cleaned_data.get("bank_account_name")
                bank_account_number = form.cleaned_data.get(
                    "bank_account_number")
                bank_name = form.cleaned_data.get("bank_name")

                promoter = Promoter()
                promoter.username = self.request.user.username
                promoter.email = self.request.user.email
                promoter.first_name = first_name
                promoter.last_name = last_name
                promoter.phone_number = phone_number
                promoter.address = address
                promoter.bank_name = bank_name
                promoter.bank_account_name = bank_account_name
                promoter.bank_account_number = bank_account_number
                promoter.save()

                if promoter.bank_name and promoter.bank_account_number and promoter.bank_account_number:
                    url = f"https://api.paystack.co/bank/resolve?account_number={promoter.bank_account_number}&bank_code={promoter.bank_name}"

                    payload = {}
                    headers = {
                        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
                    }
                    response = requests.request(
                        "GET", url, headers=headers, data=payload)
                    response = response.json()
                    if response["message"] == "Account number resolved":
                        promoter.bank_account_name = response["data"]["account_name"]
                        promoter.bank_resolved = True
                        messages.success(self.request, "Bank Account Resolved")
                    else:
                        promoter.bank_resolved = False
                        messages.warning(
                            self.request, "Bank Information not resolved, Check and try again")
                else:
                    promoter.bank_resolved = False
                promoter.save()

                messages.success(self.request, "Profile Successfully updated")

                if (promoter.username and promoter.email and promoter.first_name and promoter.last_name and promoter.phone_number and promoter.address and promoter.bank_name and promoter.bank_account_name and promoter.bank_account_number and promoter.bank_resolved):
                    promoter.complete_profile = True
                    messages.success(
                        self.request, "Profile Successfully completed")
                else:
                    promoter.complete_profile = False
                promoter.save()

        return redirect("core:profile")


class PromoterDashboardView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            promoter = Promoter.objects.get(
                username=self.request.user.username)
        except ObjectDoesNotExist:
            promoter = Promoter()
            promoter.username = self.request.user.username
            promoter.email = self.request.user.email
            promoter.save()

        referrer_qs = ReferrerOrder.objects.filter(
            promoter=promoter)
        balance = self.get_balance()
        check_status = self.get_check_status()
        total_referred = self.get_total_referred()
        transfers = self.get_transfer_requests()
        context = {
            "promoter": promoter,
            "info": referrer_qs,
            "balance": balance,
            "check_status": check_status,
            "total_referred": total_referred,
            "transfers": transfers,
        }

        return render(self.request, "account/dashboard.html", context)

    def get_balance(self, *args, **kwargs):
        balance = 0
        promoter = Promoter.objects.get(username=self.request.user.username)
        referrer_qs = ReferrerOrder.objects.filter(
            promoter=promoter, checked=False)
        for item in referrer_qs:
            balance += 200
        return balance

    def get_check_status(self, *args, **kwargs):
        checked = 0
        unchecked = 0
        promoter = Promoter.objects.get(username=self.request.user.username)
        referrer_qs = ReferrerOrder.objects.filter(
            promoter=promoter)
        for item in referrer_qs:
            if item.checked == True:
                checked += 1
            else:
                unchecked += 1
        return checked, unchecked

    def get_total_referred(self, *args, **kwargs):
        item = self.get_check_status()
        total_referred = item[0] + item[1]
        return total_referred

    def get_transfer_requests(self, *args, **kwargs):
        processed = 0
        unprocessed = 0
        promoter = Promoter.objects.get(username=self.request.user.username)
        transfer_qs = TransferRequest.objects.filter(promoter=promoter)
        for item in transfer_qs:
            if item.transfer_initialized:
                processed += 1
            else:
                unprocessed += 1
        return processed, unprocessed


class ReferredView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        promoter = Promoter.objects.get(username=self.request.user.username)
        referrer_qs = ReferrerOrder.objects.filter(
            promoter=promoter)
        transferRequests_qs = TransferRequest.objects.filter(promoter=promoter)
        bank = BANK_CHOICES
        context = {
            "bank": bank,
        }
        if referrer_qs.exists():
            context.update({
                "info": referrer_qs,
            })
        if transferRequests_qs.exists():
            context.update({
                "transfer_requests": transferRequests_qs,
            })

        return render(self.request, "account/referred.html", context)


class CashoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            promoter = Promoter.objects.get(
                username=self.request.user.username)
            for bank in BANK_CHOICES:
                if bank[0] == promoter.bank_name:
                    bank_name = bank[1]
            balance = PromoterDashboardView(request=self.request).get_balance()
            context = {
                "promoter": promoter,
                "balance": balance,
                "bank_name": bank_name,
            }
            return render(self.request, "account/cashout.html", context)
        except:
            messages.warning(self.request, "Complete your profile")
            return redirect("core:dashboard")

    def post(self, *args, **kwargs):
        promoter = Promoter.objects.get(username=self.request.user.username)
        if promoter.bank_resolved:
            try:
                accountInfo = AccountInfo.objects.get(promoter=promoter)
                if accountInfo.bank_account_number != promoter.bank_account_number:
                    accountInfo.bank_name = promoter.bank_name
                    accountInfo.bank_account_number = promoter.bank_account_number
                    accountInfo.bank_account_name = promoter.bank_account_name

                    url = "https://api.paystack.co/transferrecipient"

                    payload = {'type': 'nuban',
                               'name': promoter.bank_account_name,
                               'account_number': promoter.bank_account_number,
                               'bank_code': promoter.bank_name,
                               'currency': 'NGN'}
                    payload = json.dumps(payload)
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
                    }
                    response = requests.request(
                        "POST", url, headers=headers, data=payload)

                    response = response.json()
                    if response["message"] == "Transfer recipient created successfully":
                        accountInfo.recipient_code = response["data"]["recipient_code"]
                        accountInfo.save()

                    else:
                        messages.error(
                            self.request, "Unable to create Transfer Receipient. Try again later")
                        return redirect("core:dashboard")
            except:
                accountInfo = AccountInfo()
                accountInfo.promoter = promoter
                accountInfo.bank_name = promoter.bank_name
                accountInfo.bank_account_number = promoter.bank_account_number
                accountInfo.bank_account_name = promoter.bank_account_name

                url = "https://api.paystack.co/transferrecipient"

                payload = {'type': 'nuban',
                           'name': promoter.bank_account_name,
                           'account_number': promoter.bank_account_number,
                           'bank_code': promoter.bank_name,
                           'currency': 'NGN'}
                payload = json.dumps(payload)
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
                }
                response = requests.request(
                    "POST", url, headers=headers, data=payload)
                print(response.text)

                response = response.json()
                if response["message"] == "Transfer recipient created successfully":
                    accountInfo.recipient_code = response["data"]["recipient_code"]
                    accountInfo.save()

                else:
                    messages.error(
                        self.request, "Unable to create Transfer Receipient. Try again later")
                    return redirect("core:dashboard")

            amount = 0
            promoter = Promoter.objects.get(
                username=self.request.user.username)
            referrer_qs = ReferrerOrder.objects.filter(
                promoter=promoter, checked=False)
            for item in referrer_qs:
                amount += 200
                item.checked = True
                item.save()

            transfer_request = TransferRequest()
            transfer_request.promoter = promoter
            transfer_request.bank_name = promoter.bank_name
            transfer_request.bank_account_number = accountInfo.bank_account_number
            transfer_request.bank_account_name = accountInfo.bank_account_name
            transfer_request.amount = amount
            transfer_request.save()

            messages.success(
                self.request, "Your Transaction will be processed within the next 24 hours")

            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            client = Client(account_sid, auth_token)

            message = client.messages \
                            .create(
                                body=f"Promoter {transfer_request.promoter.first_name} has requested a cash transfer of N{transfer_request.amount}.",
                                from_=settings.TWILIO_PHONE_NUMBER,
                                to='+2348139002724'
                            )

            return redirect("core:dashboard")
        else:
            messages.error(self.request, "Access Denied")
        return redirect("core:dashboard")


def download(request, *args, **argv):
    try:
        LATEST_UPDATE = FlexibleData.objects.get(key="LATEST_VERSION").value
    except:
        LATEST_UPDATE = "1.0"
    context = {
        "LATEST_UPDATE": LATEST_UPDATE,
    }
    try:
        GOOGLE_DRIVE_LINK = FlexibleData.objects.get(
            key="GOOGLE_DRIVE_LINK").value
        context.update({"GOOGLE_DRIVE_LINK": GOOGLE_DRIVE_LINK})
    except:
        pass
    try:
        MEGA_LINK = FlexibleData.objects.get(
            key="MEGA_LINK").value
        context.update({"MEGA_LINK": MEGA_LINK})
    except:
        pass
    try:
        DATAFILEHOST_LINK = FlexibleData.objects.get(
            key="DATAFILEHOST_LINK").value
        context.update({"DATAFILEHOST_LINK": DATAFILEHOST_LINK})
    except:
        pass
    try:
        FILE_NAME = FlexibleData.objects.get(
            key="FILE_NAME").value
        context.update({"FILE_NAME": FILE_NAME})
    except:
        pass

    return render(request, "download.html", context)


def handler404(request, *args, **argv):
    context = {}
    response = render(request, "404.html", context=context)
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    context = {}
    response = render(request, "Error500.html", context=context)
    response.status_code = 500
    return response


def handler400(request, *args, **argv):
    context = {}
    response = render(request, "Error400.html", context=context)
    response.status_code = 400
    return response


def handler403(request, *args, **argv):
    context = {}
    response = render(request, "Error403.html", context=context)
    response.status_code = 403
    return response
