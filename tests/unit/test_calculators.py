import pytest
from datetime import datetime, timedelta, timezone
from app.models.checkout import Coupon, DeliveryZone, LoyaltyAccount
from app.models.cart import Cart, CartItem
from app.services.calculators.price_engine import PriceEngine

def test_price_engine_subtotal():
    engine = PriceEngine(tax_rate=0.0)
    cart = Cart(subtotal=0, total=0)
    cart.items = [
        CartItem(total_price=10.0),
        CartItem(total_price=15.0)
    ]
    
    calculated = engine.calculate_totals(cart)
    assert calculated.subtotal == 25.0
    assert calculated.total == 25.0

def test_price_engine_coupon_percentage():
    engine = PriceEngine(tax_rate=0.0)
    cart = Cart(subtotal=0, total=0)
    cart.items = [CartItem(total_price=100.0)]
    
    coupon = Coupon(discount_type="percentage", discount_value=20.0, min_order=0)
    
    calculated = engine.calculate_totals(cart, coupon=coupon)
    assert calculated.discount == 20.0
    assert calculated.total == 80.0

def test_price_engine_tax():
    engine = PriceEngine(tax_rate=0.10)
    cart = Cart(subtotal=0, total=0)
    cart.items = [CartItem(total_price=100.0)]
    
    calculated = engine.calculate_totals(cart)
    assert calculated.subtotal == 100.0
    assert calculated.tax == 10.0
    assert calculated.total == 110.0
