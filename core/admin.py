from django.contrib import admin
from .models import Customer, Order, Promoter, ReferrerOrder, AccountInfo, TransferRequest, TrialInstance, FlexibleData

# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "number_of_devices",
        "number_of_registered_devices",
        "device",
    )
    search_fields = ("first_name", "last_name", "email", "phone_number")


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "reference",
        "status",
        "amount",
        "paid_at",
        "referrer",
    )
    list_display_links = ("customer", "reference")
    list_filter = ("referrer", "status")
    search_fields = (
        "reference",
        "paid_at",
        "referrer",
        "paid_at"
    )


class PromoterAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "address",
        "bank_account_name",
        "bank_account_number",
        "bank_name",
        "complete_profile",
    )
    list_filter = (
        "complete_profile", "bank_name",
    )
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "address",
        "bank_account_name",
        "bank_account_number",
    )


class ReferrerOrderAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "order",
        "successful_payment",
        "promoter",
        "checked",
    )

    list_display_links = (
        "customer", "order", "promoter"
    )
    list_filter = (
        "successful_payment", "checked"
    )


class AccountInfoAdmin(admin.ModelAdmin):
    list_display = (
        "promoter",
        "bank_name",
        "bank_account_number",
        "bank_account_name",
        "recipient_code",
    )
    search_fields = (
        "promoter",
        "bank_name",
        "bank_account_number",
        "bank_account_name",
        "recipient_code",
    )


class TransferRequestAdmin(admin.ModelAdmin):
    list_display = (
        "promoter",
        "bank_name",
        "bank_account_number",
        "bank_account_name",
        "time",
        "amount",
        "transfer_initialized",
        "transfer_successful",
    )

    search_fields = (
        "promoter",
        "bank_account_number",
        "bank_account_name",
        "time",
        "amount",
    )

    list_filter = (
        "transfer_initialized",
        "transfer_successful",
    )


class TrialInstanceAdmin(admin.ModelAdmin):
    list_display = (
        "device_id",
        "trial_start_date",
    )

    search_fields = (
        "device_id",
    )


class FlexibleDataAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "value"
    )


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Promoter, PromoterAdmin)
admin.site.register(ReferrerOrder, ReferrerOrderAdmin)
admin.site.register(AccountInfo, AccountInfoAdmin)
admin.site.register(TransferRequest, TransferRequestAdmin)
admin.site.register(TrialInstance, TrialInstanceAdmin)
admin.site.register(FlexibleData, FlexibleDataAdmin)
