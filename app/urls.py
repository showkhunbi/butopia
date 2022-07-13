from django.urls import path
from .views import CheckCustomerExists, check_for_update, DeviceID, TrialStatus, TrialRequestView

app_name = "app"

urlpatterns = [
    path('check_customer_exists/', CheckCustomerExists.as_view(),
         name="check_customer_exists"),
    path('check_for_update/', check_for_update, name="check_for_update"),
    path('device_id/', DeviceID.as_view(), name="device_id"),
    path('trial_status/', TrialStatus.as_view(), name="device_id"),
    path('trial_request/', TrialRequestView.as_view(), name="trial_request"),
]
