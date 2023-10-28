from django.db import IntegrityError
from ninja import Router
from ninja.errors import HttpError
from ninja.pagination import PageNumberPagination, paginate
from shop import api_models, models
from http import HTTPStatus

router = Router()


@router.get(
    "/products",
    response=list[api_models.ProductOut],
    summary="Получить список товаров",
)
@paginate(PageNumberPagination, page_size=10)
def get_products(request):
    return models.Product.objects.all()


@router.post(
    "/create_order",
    summary="Создать заказ",
    response=api_models.OrderOut
)
def create_order(request, order: api_models.OrderIn):
    created_order = models.Order.objects.create(
        price=sum(product.price for product in order.products)
    )
    try:
        created_order.products.add(*(product.id for product in order.products))
    except IntegrityError:
        created_order.delete()
        raise HttpError(HTTPStatus.BAD_REQUEST, 'Wrong products ids')
    return api_models.OrderOut(id=created_order.id)
