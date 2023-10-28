from ninja import ModelSchema, Schema
from shop.models import Order, Product


class ProductOut(ModelSchema):
    class Config:
        model = Product
        model_fields = "__all__"


class ProductIn(ModelSchema):
    class Config:
        model = Product
        model_fields = ["id", "price"]


class OrderIn(Schema):
    products: list[ProductIn]


class OrderOut(ModelSchema):
    class Config:
        model = Order
        model_fields = ["id", ]
