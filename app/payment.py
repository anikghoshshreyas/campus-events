"""Structural pattern: Adapter for the payment provider.

Problem: the third-party client has an incompatible interface (cents, token).
Rejected alternative: calling the vendor client straight from the service,
which couples business logic to the vendor."""
from dataclasses import dataclass


@dataclass
class PaymentResult:
    success: bool
    reference: str = ""


class PaymentGateway:
    def pay(self, amount: float, email: str) -> PaymentResult:
        raise NotImplementedError


class LegacyVendorClient:
    """Stand-in for an external SDK we cannot change."""

    def make_charge(self, cents: int, token: str) -> dict:
        return {"ok": True, "txn": f"TXN-{cents}-{abs(hash(token)) % 10000}"}


class VendorGatewayAdapter(PaymentGateway):
    def __init__(self, client):
        self.client = client

    def pay(self, amount, email):
        resp = self.client.make_charge(int(round(amount * 100)), email)
        return PaymentResult(bool(resp.get("ok")), resp.get("txn", ""))
