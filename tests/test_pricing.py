import unittest
from datetime import date
from app.pricing import (StandardPricing, StudentDiscount, EarlyBird,
                         choose_strategy)


class PricingTests(unittest.TestCase):
    def test_standard(self):
        self.assertEqual(StandardPricing().price(200), 200)

    def test_student_discount_20_percent(self):
        self.assertEqual(StudentDiscount().price(200), 160)

    def test_early_bird_15_percent(self):
        self.assertEqual(EarlyBird().price(200), 170)

    def test_student_gets_student_strategy(self):
        s = choose_strategy("student", "2027-03-01", date(2027, 1, 1))
        self.assertIsInstance(s, StudentDiscount)

    def test_staff_early_gets_early_bird(self):
        s = choose_strategy("staff", "2027-03-01", date(2027, 1, 1))
        self.assertIsInstance(s, EarlyBird)

    def test_staff_late_pays_standard(self):
        s = choose_strategy("staff", "2027-01-03", date(2027, 1, 1))
        self.assertIsInstance(s, StandardPricing)

    def test_base_strategy_is_abstract(self):
        from app.pricing import PricingStrategy
        with self.assertRaises(NotImplementedError):
            PricingStrategy().price(1)
