from app.models.checkout import LoyaltyAccount

class LoyaltyCalculator:
    def __init__(self, points_to_currency_ratio: float = 0.01):
        self.ratio = points_to_currency_ratio

    def calculate_redeemable_amount(self, account: LoyaltyAccount) -> float:
        return account.points_balance * self.ratio
