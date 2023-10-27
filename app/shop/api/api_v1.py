from ninja import Router
from ninja.pagination import PageNumberPagination, paginate
from shop import api_models, models

router = Router()


@router.get(
    "/products",
    response=list[api_models.ProductSchema],
    tags=["products"],
    summary="Получить список товаров",
)
@paginate(PageNumberPagination, page_size=10)
def get_products(request):
    return models.Product.objects.all()
