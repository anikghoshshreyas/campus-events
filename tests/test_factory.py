import unittest
from app.factory import EventFactory
from app.models import DomainError


class EventFactoryTests(unittest.TestCase):
    def test_workshop_gets_default_fee(self):
        e = EventFactory.create("workshop", "Git 101", "2027-01-10", 30)
        self.assertEqual((e.base_fee, e.capacity), (250.0, 30))

    def test_seminar_is_free_with_default_capacity(self):
        e = EventFactory.create("seminar", "AI Talk", "2027-01-10")
        self.assertEqual((e.base_fee, e.capacity), (0.0, 300))

    def test_unknown_kind_rejected(self):
        with self.assertRaises(DomainError):
            EventFactory.create("party", "x", "2027-01-10")

    def test_bad_date_rejected(self):
        with self.assertRaises(DomainError):
            EventFactory.create("seminar", "x", "10-01-2027")

    def test_capacity_over_limit_rejected(self):
        with self.assertRaises(DomainError):
            EventFactory.create("workshop", "x", "2027-01-10", 500)

    def test_blank_title_rejected(self):
        with self.assertRaises(DomainError):
            EventFactory.create("seminar", "  ", "2027-01-10")

    def test_negative_fee_rejected(self):
        with self.assertRaises(DomainError):
            EventFactory.create("seminar", "x", "2027-01-10", fee=-5)

    def test_hackathon_defaults(self):
        e = EventFactory.create("hackathon", "CodeFest", "2027-02-10")
        self.assertEqual((e.base_fee, e.capacity), (300.0, 100))