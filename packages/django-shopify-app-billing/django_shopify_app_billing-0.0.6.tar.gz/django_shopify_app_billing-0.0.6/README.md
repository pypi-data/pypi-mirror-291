# django-shopify-app-billing

This is a Django app that provides billing for Shopify apps. It is designed to be used with the [Django Shopify App package](https://pypi.org/project/django-shopify-app/)

## Installation

```bash
pip install django-shopify-app-billing
```

Add `billing` to your `INSTALLED_APPS` in your Django settings file.

```python
INSTALLED_APPS = [
    ...
    'shopify_app_billing',
    ...
]
```

Add the following to your Shop model:

```python
from shopify_app_billing.models import ShopBilling
from shopify_app.models import ShopBase


class Shop(ShopBase):
    ...
    billing = models.OneToOneField(ShopBilling, on_delete=models.CASCADE, null=True, blank=True)
    ...

    def save(self, *args, **kwargs):
        if not self.billing:
            self.billing = ShopBilling.objects.create()

        super().save(*args, **kwargs)

    @property
    def plan_activated_redirect_path(self):
        return f"/dashboard"

```
