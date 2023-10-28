from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField(verbose_name="Название", max_length=60)
    image = models.ImageField(verbose_name="Изображение", upload_to="products/")
    content = models.TextField(verbose_name="Описание")
    price = models.DecimalField(
        verbose_name="Стоимость",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class Order(models.Model):
    price = models.DecimalField(
        verbose_name="Итоговая сумма",
        max_digits=10,
        decimal_places=2
    )

    CREATED = "CREATED"
    CONFIRMED = "CONFIRMED"
    CANCELED = "CANCELED"
    STATUS_CHOICES = (
        (CREATED, "Создан"),
        (CONFIRMED, "Подтвержден"),
        (CANCELED, "Отменен"),
    )
    status = models.CharField(
        verbose_name="Статус", max_length=10, choices=STATUS_CHOICES, default=CREATED
    )

    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)
    confirmed_at = models.DateTimeField(
        verbose_name="Время подтверждения", null=True, blank=True
    )
    products = models.ManyToManyField(
        Product, related_name="orders", verbose_name="Товары"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ №{self.id}"


class Payment(models.Model):
    amount = models.DecimalField(
        verbose_name="Сумма",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    CREATED = "CREATED"
    PAID = "PAID"
    STATUS_CHOICES = ((CREATED, "Создан"), (PAID, "Оплачен"))
    status = models.CharField(
        verbose_name="Статус", max_length=10, choices=STATUS_CHOICES, default=CREATED
    )

    CASH = "CASH"
    CARD = "CASH"
    PAYMENT_CHOICES = ((CASH, "Наличные"), (CARD, "Карта"))
    payment_type = models.CharField(
        verbose_name="Тип оплаты", max_length=4, choices=PAYMENT_CHOICES
    )

    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="payment", verbose_name="Заказ"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Платеж №{self.id}"
