from django.urls import path
from .views import ApiResponse


app_name = "phone"

urlpatterns = [
    path("response/", ApiResponse.as_view(), name="response")
]
