from ninja import ModelSchema
from shop.models import Product


class ProductSchema(ModelSchema):
    class Config:
        model = Product
        model_fields = "__all__"
