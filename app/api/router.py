from fastapi import APIRouter
from app.api.v1 import health, version, app, auth, categories, products, cart, menu, orders, hub

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(version.router, prefix="/version", tags=["Version"])
api_router.include_router(app.router, prefix="/v1/app", tags=["App Init"])
api_router.include_router(auth.router, prefix="/v1/auth", tags=["Auth"])
api_router.include_router(categories.router, prefix="/v1/categories", tags=["Categories"])
api_router.include_router(products.router, prefix="/v1/products", tags=["Products"])
api_router.include_router(menu.router, prefix="/v1/menu", tags=["Full Menu"])
api_router.include_router(cart.router, prefix="/v1/cart", tags=["Cart & Checkout"])
api_router.include_router(orders.router, prefix="/v1/orders", tags=["Orders"])
api_router.include_router(hub.router, prefix="/v1/hub", tags=["Restaurant Hub API"])
