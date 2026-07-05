from typing import Optional, List, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.cart import cart_repo, cart_item_repo
from app.repositories.menu import product_repo
from app.models.cart import Cart, CartItem
from app.models.checkout import Coupon
from app.schemas.cart import CartItemAddRequest, CartItemUpdateRequest, CartItemUpdateQuantityRequest, CartResponse
from app.services.calculators.price_engine import PriceEngine
from app.core.exceptions import BadRequestException, NotFoundException
from loguru import logger

price_engine = PriceEngine()

class CartService:
    async def get_or_create_cart(self, db: AsyncSession, customer_id: int, restaurant_id: int, branch_id: Optional[int] = None) -> Cart:
        cart = await cart_repo.get_active_cart(db, customer_id, restaurant_id)
        if not cart:
            cart = Cart(customer_id=customer_id, restaurant_id=restaurant_id, branch_id=branch_id)
            db.add(cart)
            await db.commit()
            await db.refresh(cart)
            logger.info(f"Cart Created: {cart.id} for Customer: {customer_id}")
        else:
            if branch_id and cart.branch_id and cart.branch_id != branch_id:
                raise BadRequestException("Cannot add items from a different branch to the same cart.")
            if not cart.branch_id and branch_id:
                cart.branch_id = branch_id
                await db.commit()
                await db.refresh(cart)
        return cart

    async def _get_cart_coupon(self, db: AsyncSession, cart: Cart) -> Optional[Coupon]:
        if not cart.coupon_id:
            return None
        stmt = select(Coupon).filter(Coupon.id == cart.coupon_id)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def _calculate_item_price(self, db: AsyncSession, item_request: CartItemAddRequest, restaurant_id: int) -> Tuple[float, float]:
        product = await product_repo.get_product_details(db, item_request.product_id, restaurant_id)
        if not product or not product.is_available:
            raise BadRequestException("Product is not available.")
            
        unit_price = product.base_price
        addons_total = 0.0
        
        if product.has_sizes:
            if not item_request.size_id:
                raise BadRequestException("Size selection is required.")
            size = next((s for s in product.sizes if s.id == item_request.size_id), None)
            if not size:
                raise BadRequestException("Invalid size selected.")
            unit_price = size.price
            
        requested_addons = item_request.addons or []
        grouped_requests = {}
        for addon_id in requested_addons:
            found = False
            for group in product.addon_groups:
                addon = next((a for a in group.addons if a.id == addon_id and a.is_available), None)
                if addon:
                    grouped_requests[group.id] = grouped_requests.get(group.id, 0) + 1
                    addons_total += addon.price
                    found = True
                    break
            if not found:
                raise BadRequestException(f"Addon {addon_id} is invalid or unavailable.")
                
        for group in product.addon_groups:
            count = grouped_requests.get(group.id, 0)
            if count < group.minimum_required:
                raise BadRequestException(f"Minimum {group.minimum_required} addons required for {group.name_en}.")
            if count > group.maximum_allowed:
                raise BadRequestException(f"Maximum {group.maximum_allowed} addons allowed for {group.name_en}.")
                
        return unit_price, addons_total

    async def add_item(self, db: AsyncSession, customer_id: int, restaurant_id: int, branch_id: int, item_request: CartItemAddRequest) -> CartResponse:
        cart = await self.get_or_create_cart(db, customer_id, restaurant_id, branch_id)
        
        unit_price, addons_total = await self._calculate_item_price(db, item_request, restaurant_id)
        final_unit_price = unit_price + addons_total
        
        existing_item = await cart_item_repo.get_cart_item(db, cart.id, item_request.product_id, item_request.size_id)
        if existing_item:
            existing_item.quantity += item_request.quantity
            existing_item.unit_price = final_unit_price
            existing_item.addons_total = addons_total * existing_item.quantity
            existing_item.total_price = existing_item.quantity * final_unit_price
            if item_request.notes:
                existing_item.notes = item_request.notes
            if item_request.addons:
                existing_item.addons = item_request.addons
            logger.info(f"Item Updated: {existing_item.id} in Cart: {cart.id}")
        else:
            new_item = CartItem(
                cart_id=cart.id,
                product_id=item_request.product_id,
                size_id=item_request.size_id,
                quantity=item_request.quantity,
                unit_price=final_unit_price,
                addons_total=addons_total * item_request.quantity,
                total_price=final_unit_price * item_request.quantity,
                notes=item_request.notes,
                addons=item_request.addons
            )
            db.add(new_item)
            logger.info(f"Item Added: Product {item_request.product_id} to Cart: {cart.id}")
            
        await db.commit()
        await db.refresh(cart)
        
        coupon = await self._get_cart_coupon(db, cart)
        cart = price_engine.calculate_totals(cart, coupon=coupon)
        await db.commit()
        await db.refresh(cart)
        return CartResponse.model_validate(cart)

    async def update_item_quantity(self, db: AsyncSession, customer_id: int, restaurant_id: int, item_id: int, quantity: int) -> CartResponse:
        cart = await cart_repo.get_active_cart(db, customer_id, restaurant_id)
        if not cart:
            raise NotFoundException("Cart not found.")
            
        item = next((i for i in cart.items if i.id == item_id), None)
        if not item:
            raise NotFoundException("Item not found in cart.")
            
        item.quantity = quantity
        item.addons_total = (item.addons_total / (item.quantity or 1)) * quantity if item.quantity > 0 else 0
        item.total_price = item.quantity * item.unit_price
        
        await db.commit()
        await db.refresh(cart)
        
        coupon = await self._get_cart_coupon(db, cart)
        cart = price_engine.calculate_totals(cart, coupon=coupon)
        await db.commit()
        await db.refresh(cart)
        return CartResponse.model_validate(cart)

    async def remove_item(self, db: AsyncSession, customer_id: int, restaurant_id: int, item_id: int) -> CartResponse:
        cart = await cart_repo.get_active_cart(db, customer_id, restaurant_id)
        if not cart:
            raise NotFoundException("Cart not found.")
            
        item = next((i for i in cart.items if i.id == item_id), None)
        if not item:
            raise NotFoundException("Item not found in cart.")
            
        await cart_item_repo.delete(db, id=item_id)
        
        await db.refresh(cart)
        if not cart.items:
            cart.branch_id = None
            cart.coupon_id = None
            
        coupon = await self._get_cart_coupon(db, cart)
        cart = price_engine.calculate_totals(cart, coupon=coupon)
        await db.commit()
        await db.refresh(cart)
        return CartResponse.model_validate(cart)

    async def clear_cart(self, db: AsyncSession, customer_id: int, restaurant_id: int) -> dict:
        cart = await cart_repo.get_active_cart(db, customer_id, restaurant_id)
        if not cart:
            raise NotFoundException("Cart not found.")
            
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
        return {"message": "Cart cleared successfully"}

    async def get_cart(self, db: AsyncSession, customer_id: int, restaurant_id: int) -> CartResponse:
        cart = await self.get_or_create_cart(db, customer_id, restaurant_id)
        return CartResponse.model_validate(cart)
        
    async def calculate_cart(self, db: AsyncSession, customer_id: int, restaurant_id: int) -> CartResponse:
        cart = await cart_repo.get_active_cart(db, customer_id, restaurant_id)
        if not cart:
            raise NotFoundException("Cart not found.")
            
        coupon = await self._get_cart_coupon(db, cart)
        cart = price_engine.calculate_totals(cart, coupon=coupon)
        await db.commit()
        await db.refresh(cart)
        return CartResponse.model_validate(cart)

    async def apply_coupon(self, db: AsyncSession, customer_id: int, restaurant_id: int, code: str) -> CartResponse:
        cart = await cart_repo.get_active_cart(db, customer_id, restaurant_id)
        if not cart:
            raise NotFoundException("Cart not found.")
            
        stmt = select(Coupon).filter(Coupon.code == code, Coupon.restaurant_id == restaurant_id)
        result = await db.execute(stmt)
        coupon = result.scalars().first()
        
        if not coupon:
            raise BadRequestException("Invalid coupon code.")
            
        try:
            price_engine.coupon_validator.validate_and_calculate(coupon, cart)
            cart.coupon_id = coupon.id
            cart = price_engine.calculate_totals(cart, coupon=coupon)
            await db.commit()
            await db.refresh(cart)
            return CartResponse.model_validate(cart)
        except ValueError as e:
            raise BadRequestException(str(e))

cart_service = CartService()
