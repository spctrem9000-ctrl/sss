from app.models.cart import Cart
from app.models.checkout import Coupon, DeliveryZone, LoyaltyAccount
from app.services.calculators.coupon import CouponValidator
from app.services.calculators.delivery import DeliveryCalculator
from app.services.calculators.loyalty import LoyaltyCalculator

class PriceEngine:
    def __init__(self, tax_rate: float = 0.15):
        self.tax_rate = tax_rate
        self.coupon_validator = CouponValidator()
        self.delivery_calculator = DeliveryCalculator()
        self.loyalty_calculator = LoyaltyCalculator()

    def calculate_totals(
        self, 
        cart: Cart, 
        coupon: Coupon = None, 
        delivery_zone: DeliveryZone = None,
        loyalty_account: LoyaltyAccount = None,
        redeem_loyalty: bool = False
    ) -> Cart:
        
        # 1. Subtotal
        cart.subtotal = sum(item.total_price for item in cart.items)
        cart.addons_total = sum(item.addons_total for item in cart.items)
        
        # 2. Discount
        cart.discount = 0.0
        if coupon:
            try:
                cart.discount += self.coupon_validator.validate_and_calculate(coupon, cart)
            except ValueError:
                pass # Optional: bubble up exception if strict failure is needed
                
        if redeem_loyalty and loyalty_account:
            loyalty_discount = self.loyalty_calculator.calculate_redeemable_amount(loyalty_account)
            cart.discount += min(loyalty_discount, cart.subtotal - cart.discount)
            
        cart.discount = min(cart.discount, cart.subtotal)
        
        # 3. Delivery Fee
        cart.delivery_fee = 0.0
        if delivery_zone:
            cart.delivery_fee = self.delivery_calculator.calculate_fee(cart.subtotal, delivery_zone)
            
        # 4. Tax
        taxable_amount = cart.subtotal - cart.discount
        cart.tax = taxable_amount * self.tax_rate
        
        # 5. Total
        cart.total = cart.subtotal - cart.discount + cart.delivery_fee + cart.tax
        
        return cart
