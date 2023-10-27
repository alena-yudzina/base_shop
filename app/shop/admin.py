from django.contrib import admin
from shop import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "content", "price")
    search_fields = ("name",)


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "price", "status", "created_at", "confirmed_at")
    readonly_fields = ("created_at", "confirmed_at")
    filter_horizontal = ("products",)
    list_filter = ("status",)
    search_fields = ("id",)


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "amount", "status", "payment_type", "order")
    list_filter = ("status", "payment_type")
    autocomplete_fields = ("order",)
