from audioop import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.clickjacking import xframe_options_exempt


from .services import get_managed_pricing_plans, activate_recuring_charge

from shopify_app.decorators import shopify_embed, known_shop_required
from shopify_app.utils import shopify_app_redirect


@xframe_options_exempt
def plans_redirect(request):
    return redirect(get_managed_pricing_plans())


@shopify_embed
@known_shop_required
@xframe_options_exempt
def activate_plan(request, *args, **kwargs):

    shop = request.shop
    recurring_charge_id = request.GET.get("charge_id")
    if not shop or not recurring_charge_id:
        return redirect("shopify_app_billing:plans")

    plan = activate_recuring_charge(shop, recurring_charge_id)

    if plan["status"] == "active":
        return shopify_app_redirect(
            request,
            f"{shop.plan_activated_redirect_path}?{request.GET.urlencode()}",
            shop,
        )
    else:

        plans_url = reverse("shopify_app_billing:plans")
        return shopify_app_redirect(request, plans_url, shop)
