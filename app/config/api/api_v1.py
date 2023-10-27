from ninja import NinjaAPI
from shop.api.api_v1 import router as shop_router

api = NinjaAPI(version="1.0.0")

api.add_router("/shop/", shop_router)
