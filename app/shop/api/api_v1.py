from django.db import transaction
from ninja import Router
from ninja.pagination import PageNumberPagination, paginate
from shop import models
from shop.api import schemas

router = Router()


@router.get(
    "/products",
    response=list[schemas.ProductOut],
    summary="Получить список товаров",
)
@paginate(PageNumberPagination, page_size=10)
def get_products(request):
    return models.Product.objects.all()


@transaction.atomic
@router.post("/create_order", summary="Создать заказ", response=schemas.OrderOut)
def create_order(request, order: schemas.OrderIn):
    created_order = models.Order.objects.create(
        price=sum(product.price for product in order.products)
    )
    products_ids = [product.id for product in order.products]
    created_order.products.add(*products_ids)
    return schemas.OrderOut(id=created_order.id)


@router.post("/create_payment", summary="Создать платеж", response=schemas.PaymentOut)
def create_payment(request, payment: schemas.PaymentIn):
    order = models.Order.objects.get(id=payment.order_id)
    payment = models.Payment.objects.create(
        amount=order.price, payment_type=payment.payment_type, order=order
    )
    return schemas.PaymentOut(id=payment.id)
