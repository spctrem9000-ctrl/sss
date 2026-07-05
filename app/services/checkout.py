import string
import random
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order import Order, OrderItem, OrderStatusHistory
from app.repositories.cart import cart_repo
from app.services.cart import cart_service
from app.schemas.order import CheckoutRequest, OrderResponse
from app.core.exceptions import BadRequestException, NotFoundException

def generate_order_number() -> str:
    chars = string.ascii_uppercase + string.digits
    return "ORD-" + "".join(random.choice(chars) for _ in range(8))

class CheckoutService:
    async def process_checkout(
        self, 
        db: AsyncSession, 
        customer_id: int, 
        restaurant_id: int, 
        request: CheckoutRequest
    ) -> OrderResponse:
        # Fetch cart directly rather than recalculating to avoid validation errors bubbling unexpectedly, 
        # but calculate guarantees the price is perfectly fresh.
        cart_resp = await cart_service.calculate_cart(db, customer_id, restaurant_id)
        cart = await cart_repo.get_active_cart(db, customer_id, restaurant_id)
        
        if not cart or not cart.items:
            raise BadRequestException("Cart is empty.")
            
        if not cart.branch_id:
            raise BadRequestException("Branch ID is required but cart is not associated with any branch.")
            
        try:
            new_order = Order(
                order_number=generate_order_number(),
                restaurant_id=restaurant_id,
                customer_id=customer_id,
                branch_id=cart.branch_id,
                coupon_id=cart.coupon_id,
                status="NEW",
                subtotal=cart.subtotal,
                addons_total=cart.addons_total,
                discount=cart.discount,
                delivery_fee=cart.delivery_fee,
                tax=cart.tax,
                total=cart.total,
                payment_method=request.payment_method
            )
            db.add(new_order)
            await db.flush()
            
            for item in cart.items:
                order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=item.product_id,
                    size_id=item.size_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    addons_total=item.addons_total,
                    total_price=item.total_price,
                    notes=item.notes,
                    addons=item.addons
                )
                db.add(order_item)
                
            history = OrderStatusHistory(
                order_id=new_order.id,
                old_status=None,
                new_status="NEW",
                created_by=customer_id
            )
            db.add(history)
            
            # Clear Cart
            for item in cart.items:
                await db.delete(item)
            cart.branch_id = None
            cart.coupon_id = None
            cart.subtotal = 0.0
            cart.addons_total = 0.0
            cart.discount = 0.0
            cart.delivery_fee = 0.0
            cart.tax = 0.0
            cart.total = 0.0
            
            await db.commit()
            await db.refresh(new_order)
            
            return OrderResponse.model_validate(new_order)
        except Exception as e:
            await db.rollback()
            raise BadRequestException(f"Checkout failed: {str(e)}")

checkout_service = CheckoutService()
