import json
from unittest.mock import MagicMock, patch

from django.test import Client, TestCase
from shop.admin import approve_order
from shop.models import Order, Payment, Product


class ProductTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_empty_get_products(self):
        expected_json = {"count": 0, "items": []}

        result = self.client.get("http://127.0.0.1:8000/api/v1/shop/products?page=1")

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), expected_json)

    def test_get_products(self):
        Product.objects.create(name="product_1", content="content_1", price=1000)
        Product.objects.create(name="product_2", content="content_2", price=2000)
        expected_json = {
            "count": 2,
            "items": [
                {
                    "content": "content_1",
                    "id": 1,
                    "image": None,
                    "name": "product_1",
                    "price": "1000.00",
                },
                {
                    "content": "content_2",
                    "id": 2,
                    "image": None,
                    "name": "product_2",
                    "price": "2000.00",
                },
            ],
        }

        result = self.client.get("http://127.0.0.1:8000/api/v1/shop/products?page=1")

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), expected_json)


class OrderTests(TestCase):
    def setUp(self) -> None:
        self.product_1 = Product.objects.create(
            name="product_1", content="content_1", price=1000
        )
        self.product_2 = Product.objects.create(
            name="product_2", content="content_2", price=2000
        )
        self.client = Client()

    def test_create_order(self):
        order_data = {
            "products": [
                {"id": self.product_1.id, "price": self.product_1.price},
                {"id": self.product_2.id, "price": self.product_2.price},
            ]
        }
        expected_json = {"id": 1}

        result = self.client.post(
            "http://127.0.0.1:8000/api/v1/shop/create_order",
            data=json.dumps(order_data),
            content_type="json",
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), expected_json)
        self.assertEqual(Order.objects.all().count(), 1)
        self.assertEqual(Order.objects.first().products.count(), 2)

    def test_create_order_wrong_product_id(self):
        order_data = {
            "products": [
                {"id": 3231, "price": self.product_1.price},
                {"id": self.product_2.id, "price": self.product_2.price},
            ]
        }
        expected_json = {
            "detail": [
                {
                    "loc": ["body", "order", "products", 0, "id"],
                    "msg": "Wrong product id: 3231",
                    "type": "value_error",
                }
            ]
        }

        result = self.client.post(
            "http://127.0.0.1:8000/api/v1/shop/create_order",
            data=json.dumps(order_data),
            content_type="json",
        )

        self.assertEqual(result.status_code, 422)
        self.assertEqual(result.json(), expected_json)
        self.assertEqual(Order.objects.all().count(), 0)


class PaymentTests(TestCase):
    def setUp(self) -> None:
        self.product_1 = Product.objects.create(
            name="product_1", content="content_1", price=1000
        )
        self.product_2 = Product.objects.create(
            name="product_2", content="content_2", price=2000
        )
        self.order = Order.objects.create(
            price=self.product_1.price + self.product_2.price
        )
        self.order.products.add(self.product_1.id, self.product_2.id)
        self.client = Client()

    def test_create_payment(self):
        payment_data = {"order_id": self.order.id, "payment_type": "CASH"}
        expected_json = {"id": 1}

        result = self.client.post(
            "http://127.0.0.1:8000/api/v1/shop/create_payment",
            data=json.dumps(payment_data),
            content_type="json",
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), expected_json)
        self.assertEqual(Payment.objects.all().count(), 1)
        self.assertEqual(Payment.objects.first().order, self.order)

    def test_create_payment_wrong_order_id(self):
        payment_data = {"order_id": 3231, "payment_type": "CASH"}
        expected_json = {
            "detail": [
                {
                    "loc": ["body", "payment", "order_id"],
                    "msg": "Wrong order id: 3231",
                    "type": "value_error",
                }
            ]
        }

        result = self.client.post(
            "http://127.0.0.1:8000/api/v1/shop/create_payment",
            data=json.dumps(payment_data),
            content_type="json",
        )

        self.assertEqual(result.status_code, 422)
        self.assertEqual(result.json(), expected_json)
        self.assertEqual(Payment.objects.all().count(), 0)

    def test_create_payment_wrong_payment_type(self):
        payment_data = {"order_id": self.order.id, "payment_type": "FAIL"}
        expected_json = {
            "detail": [
                {
                    "loc": ["body", "payment", "payment_type"],
                    "msg": "value is not a valid enumeration member; permitted: 'CASH', 'CARD'",
                    "type": "type_error.enum",
                    "ctx": {"enum_values": ["CASH", "CARD"]},
                }
            ]
        }

        result = self.client.post(
            "http://127.0.0.1:8000/api/v1/shop/create_payment",
            data=json.dumps(payment_data),
            content_type="json",
        )
        self.assertEqual(result.status_code, 422)
        self.assertEqual(result.json(), expected_json)
        self.assertEqual(Payment.objects.all().count(), 0)


class ApproveOrderTests(TestCase):
    @patch("shop.models.Order.save")
    @patch("shop.admin.settings.APPROVE_ORDER_URL", "http://example.com/approve-order")
    @patch("requests.post")
    def test_approve_order_success(self, mock_post, mock_save):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        order = Order(id=1, price=10.0, status=Order.CREATED)
        result = approve_order(order)

        self.assertTrue(result)
        mock_post.assert_called_once_with(
            "http://example.com/approve-order",
            data={"id": 1, "amount": 10.0, "date": order.confirmed_at},
        )
        mock_save.assert_called_once()

    @patch("shop.models.Order.save")
    @patch("shop.admin.settings.APPROVE_ORDER_URL", "http://example.com/approve-order")
    @patch("requests.post")
    def test_approve_order_failure(self, mock_post, mock_save):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        order = Order(id=1, price=10.0, status=Order.CREATED)
        result = approve_order(order)

        self.assertFalse(result)
        mock_post.assert_called_once_with(
            "http://example.com/approve-order",
            data={"id": 1, "amount": 10.0, "date": order.confirmed_at},
        )
        mock_save.assert_not_called()
