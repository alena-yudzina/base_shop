from django.core.management.base import BaseCommand
from shop.models import Order, Payment, Product


class Command(BaseCommand):
    help = "Fill the database with fake data"

    def handle(self, *args, **options):

        t_shirt = Product.objects.create(
            name="Футболка", content="Классная", price=1500.55
        )
        jacket = Product.objects.create(
            name="Куртка", content="Теплая", price=5000
        )

        paid_order = Order.objects.create(price=6500.55)
        paid_order.products.add(t_shirt.id, jacket.id)
        Payment.objects.create(amount=6500.55, status=Payment.PAID, payment_type=Payment.CASH, order=paid_order)

        unpaid_order = Order.objects.create(price=6500.55)
        unpaid_order.products.add(t_shirt.id, jacket.id)
