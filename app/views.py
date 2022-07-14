from django.shortcuts import render
from django.shortcuts import HttpResponse
from core.models import Customer, TrialInstance, FlexibleData
from .models import TrialRequest
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import datetime

try:
    LATEST_UPDATE = FlexibleData.objects.get(key="LATEST_VERSION").value
except:
    LATEST_UPDATE = "1.0"


@method_decorator(csrf_exempt, name='dispatch')
class CheckCustomerExists(View):
    def post(self, request):

        email = request.POST["email"]
        if email != "" and ("@" in email):
            customer = Customer.objects.filter(email=email)
            if customer.exists():
                return HttpResponse("customer exists")
            else:
                return HttpResponse("customer does not exist")
        else:
            return HttpResponse("Email is Invalid")


def check_for_update(request):
    return HttpResponse(LATEST_UPDATE)


@method_decorator(csrf_exempt, name='dispatch')
class DeviceID(View):
    def post(self, request):
        email = request.POST["email"]
        device_id = request.POST["device_id"]

        if email != "" and ("@" in email):
            customer = Customer.objects.filter(email=email)
            if customer.exists():
                customer = Customer.objects.get(email=email)
                if customer.device == None:
                    device = ""
                else:
                    device = customer.device

                if device_id != "":
                    if device_id not in device.split(", "):
                        if customer.number_of_devices > customer.number_of_registered_devices:
                            customer.device = device + device_id + ", "
                            customer.number_of_registered_devices += 1
                            customer.save()
                            return HttpResponse("New device registered")
                        else:
                            return HttpResponse("redirect to payment")
                    else:
                        return HttpResponse("customer confirmed")
                else:
                    return HttpResponse("Invalid device id")
            else:
                return HttpResponse("customer does not exist")
        else:
            return HttpResponse("Email is invalid")


@method_decorator(csrf_exempt, name='dispatch')
class TrialStatus(View):
    def post(self, request):
        device_id = request.POST["device_id"]
        trial_start_date = request.POST["trial_start_date"]

        trialInstance = TrialInstance.objects.filter(device_id=device_id)
        if trialInstance.exists():
            trialInstance = TrialInstance.objects.get(device_id=device_id)

            now = datetime.datetime.now() + datetime.timedelta(hours=1)
            time = datetime.datetime.strptime(
                trialInstance.trial_start_date, "%Y-%m-%dT%H:%M:%S.%f")
            diff = (now - time).total_seconds()
            if diff >= 86400:
                status = "Expired"
            elif diff < 86400 and diff >= 0:
                status = "In Trial"
            elif diff < 0:
                status = "Expired"
            response = "trial_date_info," + trialInstance.trial_start_date + "," + status
            return HttpResponse(response)

        else:
            trial = TrialInstance()
            trial.device_id = device_id
            trial.trial_start_date = trial_start_date
            trial.save()
            return HttpResponse("start new trial")


@method_decorator(csrf_exempt, name='dispatch')
class TrialRequestView(View):
    def post(self, request):
        email = request.POST["email"]
        pseudoID = request.POST["pseudoId"]
        deviceInformation = request.POST["deviceInformation"]

        try:
            a = TrialRequest(email=email, pseudoID=pseudoID,
                             deviceInformation=deviceInformation)
            a.save()
            return HttpResponse("Success")
        except:
            return HttpResponse("Error Occured")
