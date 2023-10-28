from http import HTTPStatus

from django.db import IntegrityError
from ninja import Router
from ninja.errors import HttpError
from ninja.pagination import PageNumberPagination, paginate
from shop import api_models, models

router = Router()


@router.get(
    "/products",
    response=list[api_models.ProductOut],
    summary="Получить список товаров",
)
@paginate(PageNumberPagination, page_size=10)
def get_products(request):
    return models.Product.objects.all()


@router.post("/create_order", summary="Создать заказ", response=api_models.OrderOut)
def create_order(request, order: api_models.OrderIn):
    created_order = models.Order.objects.create(
        price=sum(product.price for product in order.products)
    )
    try:
        created_order.products.add(*(product.id for product in order.products))
    except IntegrityError:
        created_order.delete()
        raise HttpError(HTTPStatus.BAD_REQUEST, "Wrong products ids")
    return api_models.OrderOut(id=created_order.id)


@router.post(
    "/create_payment", summary="Создать платеж", response=api_models.PaymentOut
)
def create_payment(request, payment: api_models.PaymentIn):
    order = models.Order.objects.filter(id=payment.order_id).first()
    if not order:
        raise HttpError(HTTPStatus.BAD_REQUEST, "Wrong order id")
    try:
        payment = models.Payment.objects.create(
            amount=order.price, payment_type=payment.payment_type, order=order
        )
    except IntegrityError:
        raise HttpError(HTTPStatus.BAD_REQUEST, "Payment already exists")
    return api_models.PaymentOut(id=payment.id)
