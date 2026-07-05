from datetime import datetime, timezone
from app.models.checkout import Coupon
from app.models.cart import Cart

class CouponValidator:
    def validate_and_calculate(self, coupon: Coupon, cart: Cart) -> float:
        """Validates a coupon against a cart and returns the discount amount."""
        if coupon.restaurant_id != cart.restaurant_id:
            raise ValueError("Coupon is not valid for this restaurant")
            
        if coupon.branch_id and coupon.branch_id != cart.branch_id:
            raise ValueError("Coupon is not valid for this branch")
        if coupon.expires_at and coupon.expires_at < datetime.now(timezone.utc):
            raise ValueError("Coupon has expired")
            
        if cart.subtotal < coupon.min_order:
            raise ValueError(f"Minimum order amount is {coupon.min_order}")
            
        if coupon.usage_limit is not None and coupon.usage_limit <= 0:
            raise ValueError("Coupon usage limit reached")
            
        discount = 0.0
        if coupon.discount_type == "percentage":
            discount = cart.subtotal * (coupon.discount_value / 100.0)
            if coupon.max_discount and discount > coupon.max_discount:
                discount = coupon.max_discount
        elif coupon.discount_type == "fixed":
            discount = coupon.discount_value
            
        return discount
