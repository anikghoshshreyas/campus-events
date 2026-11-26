import unittest
from unittest.mock import Mock
from app.payment import VendorGatewayAdapter, PaymentGateway, LegacyVendorClient


class AdapterTests(unittest.TestCase):
    def test_converts_amount_to_cents(self):
        client = Mock()
        client.make_charge.return_value = {"ok": True, "txn": "T1"}
        res = VendorGatewayAdapter(client).pay(160.5, "a@b.c")
        client.make_charge.assert_called_once_with(16050, "a@b.c")
        self.assertTrue(res.success)
        self.assertEqual(res.reference, "T1")

    def test_failure_is_reported(self):
        client = Mock()
        client.make_charge.return_value = {"ok": False}
        self.assertFalse(VendorGatewayAdapter(client).pay(10, "a@b.c").success)

    def test_interface_is_abstract(self):
        with self.assertRaises(NotImplementedError):
            PaymentGateway().pay(1, "x")

    def test_legacy_client_stub(self):
        self.assertTrue(LegacyVendorClient().make_charge(100, "t")["ok"])
