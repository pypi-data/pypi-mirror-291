from django.apps import AppConfig


class ShopifyAppBillingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shopify_app_billing"

    def ready(self):
        pass
