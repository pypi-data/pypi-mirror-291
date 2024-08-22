from django.db import models


class RecurringApplicationCharge(models.Model):

    shop_billing = models.ForeignKey(
        "shopify_app_billing.ShopBilling",
        on_delete=models.CASCADE,
        related_name="recurring_application_charges",
    )

    shopify_rest_id = models.BigIntegerField(
        default=None,
        null=False,
        blank=False,
    )
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
    )
    status = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )
    test = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )
    currency = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )

    class Meta:
        constraints = [
            models.constraints.UniqueConstraint(
                fields=["shop_billing", "shopify_rest_id"],
                name="unique_shop_billing_shopify_rest_id",
            ),
        ]

    def __str__(self):
        return f"{self.name} for {self.shop_billing.shop}"
