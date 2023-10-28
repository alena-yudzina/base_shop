from enum import Enum

from ninja import ModelSchema, Schema
from shop.models import Order, Payment, Product


class ProductIn(ModelSchema):
    class Config:
        model = Product
        model_fields = ["id", "price"]


class ProductOut(ModelSchema):
    class Config:
        model = Product
        model_fields = "__all__"


class OrderIn(Schema):
    products: list[ProductIn]


class OrderOut(ModelSchema):
    class Config:
        model = Order
        model_fields = [
            "id",
        ]


class ProductIn(ModelSchema):
    class Config:
        model = Product
        model_fields = ["id", "price"]


class PaymentTypes(str, Enum):
    CASH = "CASH"
    CARD = "CARD"


class PaymentIn(Schema):
    order_id: int
    payment_type: PaymentTypes


class PaymentOut(ModelSchema):
    class Config:
        model = Payment
        model_fields = [
            "id",
        ]
