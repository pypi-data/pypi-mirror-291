from django.contrib import admin

from .services import on_app_uninstall, update_all_charges
from .models import ShopBilling, RecurringApplicationCharge


@admin.register(ShopBilling)
class ShopBillingAdmin(admin.ModelAdmin):

    list_display = [
        "__str__",
        "has_active_billing",
        "active_recurring_application_charge_price",
    ]
    actions = ["update_all_charges", "on_app_uninstall"]

    def update_all_charges(self, request, queryset):
        for shop_billing in queryset:
            update_all_charges(shop_billing.shop)
        self.message_user(request, "All charges were updated.")

    def on_app_uninstall(self, request, queryset):
        for shop_billing in queryset:
            on_app_uninstall(shop_billing.shop)
        self.message_user(request, "All active charges were cancelled.")


@admin.register(RecurringApplicationCharge)
class RecurringApplicationChargeAdmin(admin.ModelAdmin):
    list_display = ("name", "shop_billing", "price", "status", "test", "currency")
    list_filter = ("status", "test")
