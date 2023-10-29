from enum import Enum
from typing import Generic, TypeVar

from ninja import ModelSchema, Schema
from pydantic.fields import ModelField
from shop.models import Order, Payment, Product

PydanticField = TypeVar("PydanticField")


class ExistingProductID(Generic[PydanticField]):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, product_id: PydanticField, field: ModelField) -> PydanticField:
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValueError(f"Wrong product id: {product_id}")
        return product_id


class ExistingOrderID(Generic[PydanticField]):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, order_id: PydanticField, field: ModelField) -> PydanticField:
        try:
            Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise ValueError(f"Wrong order id: {order_id}")
        return order_id


class ProductIn(Schema):
    id: ExistingProductID[int]
    price: float


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


class PaymentTypes(str, Enum):
    CASH = "CASH"
    CARD = "CARD"


class PaymentIn(Schema):
    order_id: ExistingOrderID[int]
    payment_type: PaymentTypes


class PaymentOut(ModelSchema):
    class Config:
        model = Payment
        model_fields = [
            "id",
        ]
