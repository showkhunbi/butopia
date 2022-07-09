from django.contrib import admin
from .models import TrialRequest
# Register your models here.


class TrialRequestAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "pseudoID",
        "deviceInformation",
        "time",
        "checked",
        "approved",
    )

    search_fields = (
        "email",
        "pseudoID",
        "deviceInformation",
    )

    list_filter = (
        "checked",
        "approved",
    )


admin.site.register(TrialRequest, TrialRequestAdmin)
