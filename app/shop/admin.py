import time
from datetime import datetime

import requests
from django.conf import settings
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from requests.exceptions import HTTPError
from shop import models


def approve_order(order: models.Order) -> bool:
    order.status = models.Order.CONFIRMED
    order.confirmed_at = datetime.now()

    time.sleep(3)

    url = settings.APPROVE_ORDER_URL
    body = {"id": order.id, "amount": float(order.price), "date": order.confirmed_at}
    response = requests.post(url, data=body)
    try:
        response.raise_for_status()
    except HTTPError:
        return False

    order.save()
    return True


class PaymentInline(admin.TabularInline):
    model = models.Payment
    extra = 0


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "content", "price")
    search_fields = ("name",)


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "price", "status", "created_at", "confirmed_at", "_is_paid")
    readonly_fields = ("created_at", "confirmed_at")
    filter_horizontal = ("products",)
    list_filter = ("status",)
    search_fields = ("id",)
    inlines = (PaymentInline,)

    def response_change(self, request, obj):
        if "_approve" in request.POST:
            is_approved = approve_order(obj)
            if is_approved:
                self.message_user(request, "Заказ подтвержден")
            else:
                self.message_user(
                    request,
                    "Возникли проблемы с подтверждением заказа",
                    level=messages.ERROR,
                )
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "amount", "status", "payment_type", "order")
    list_filter = ("status", "payment_type")
