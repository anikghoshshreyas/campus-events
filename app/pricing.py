"""Behavioral pattern: Strategy for ticket pricing.

Problem: price rules (student discount, early bird) change often.
Rejected alternative: conditionals inside RegistrationService."""
from datetime import date


class PricingStrategy:
    def price(self, base_fee: float) -> float:
        raise NotImplementedError


class StandardPricing(PricingStrategy):
    def price(self, base_fee):
        return round(base_fee, 2)


class StudentDiscount(PricingStrategy):
    def __init__(self, percent=20):
        self.percent = percent

    def price(self, base_fee):
        return round(base_fee * (1 - self.percent / 100), 2)


class EarlyBird(PricingStrategy):
    def __init__(self, percent=15):
        self.percent = percent

    def price(self, base_fee):
        return round(base_fee * (1 - self.percent / 100), 2)


def choose_strategy(role: str, event_date: str, today: date | None = None):
    today = today or date.today()
    days_left = (date.fromisoformat(event_date) - today).days
    if role == "student":
        return StudentDiscount()
    if days_left >= 7:
        return EarlyBird()
    return StandardPricing()
