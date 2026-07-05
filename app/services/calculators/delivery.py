from app.models.checkout import DeliveryZone

class DeliveryCalculator:
    def calculate_fee(self, subtotal: float, zone: DeliveryZone) -> float:
        if subtotal < zone.min_order:
            raise ValueError(f"Minimum order for this delivery zone is {zone.min_order}")
        return zone.fee
