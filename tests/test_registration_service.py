"""Unit tests with mocks: DB repositories, payment gateway and e-mail sender
are all replaced so no database/network is touched."""
import unittest
from datetime import date
from unittest.mock import Mock
from app.models import User, Event, DomainError
from app.payment import PaymentResult
from app.services import RegistrationService, UserService
from app.notifications import EventBus, EmailNotifier


def make_service(user=None, event=None, exists=False, count=0, pay_ok=True):
    users, events, regs = Mock(), Mock(), Mock()
    users.get.return_value = user
    events.get.return_value = event
    regs.exists.return_value = exists
    regs.count_for_event.return_value = count
    regs.add.side_effect = lambda r: r
    gateway = Mock()
    gateway.pay.return_value = PaymentResult(pay_ok, "REF")
    bus = Mock()
    svc = RegistrationService(users, events, regs, gateway, bus, today=date(2027, 1, 1))
    return svc, regs, gateway, bus


STUDENT = User(1, "Rafi", "rafi@ruet.ac.bd", "student")
WORKSHOP = Event(5, "Git 101", "2027-03-01", 2, 200.0, "workshop")
SEMINAR = Event(6, "Free Talk", "2027-03-01", 2, 0.0, "seminar")


class RegistrationServiceTests(unittest.TestCase):
    def test_student_pays_discounted_price(self):
        svc, regs, gateway, bus = make_service(STUDENT, WORKSHOP)
        reg = svc.register(1, 5)
        gateway.pay.assert_called_once_with(160.0, "rafi@ruet.ac.bd")
        self.assertEqual(reg.amount_paid, 160.0)

    def test_free_event_skips_payment(self):
        svc, regs, gateway, bus = make_service(STUDENT, SEMINAR)
        svc.register(1, 6)
        gateway.pay.assert_not_called()

    def test_publishes_registered_event(self):
        svc, regs, gateway, bus = make_service(STUDENT, WORKSHOP)
        svc.register(1, 5)
        topic, payload = bus.publish.call_args[0]
        self.assertEqual(topic, "registered")
        self.assertEqual(payload["amount"], 160.0)

    def test_missing_user_or_event_is_404(self):
        svc, *_ = make_service(None, WORKSHOP)
        with self.assertRaises(DomainError) as ctx:
            svc.register(1, 5)
        self.assertEqual(ctx.exception.status, 404)

    def test_duplicate_registration_rejected(self):
        svc, *_ = make_service(STUDENT, WORKSHOP, exists=True)
        with self.assertRaises(DomainError) as ctx:
            svc.register(1, 5)
        self.assertEqual(ctx.exception.status, 409)

    def test_full_event_rejected(self):
        svc, *_ = make_service(STUDENT, WORKSHOP, count=2)
        with self.assertRaises(DomainError):
            svc.register(1, 5)

    def test_payment_failure_saves_nothing(self):
        svc, regs, gateway, bus = make_service(STUDENT, WORKSHOP, pay_ok=False)
        with self.assertRaises(DomainError) as ctx:
            svc.register(1, 5)
        self.assertEqual(ctx.exception.status, 402)
        regs.add.assert_not_called()
        bus.publish.assert_not_called()


class UserServiceTests(unittest.TestCase):
    def test_duplicate_email_rejected(self):
        repo = Mock()
        repo.by_email.return_value = STUDENT
        with self.assertRaises(DomainError):
            UserService(repo).create("A", "rafi@ruet.ac.bd")

    def test_invalid_email_rejected(self):
        with self.assertRaises(DomainError):
            UserService(Mock()).create("A", "nope")

    def test_invalid_role_rejected(self):
        with self.assertRaises(DomainError):
            UserService(Mock()).create("A", "a@b.c", "admin")

    def test_valid_user_saved(self):
        repo = Mock()
        repo.by_email.return_value = None
        repo.add.side_effect = lambda u: u
        u = UserService(repo).create(" A ", "a@b.c")
        self.assertEqual(u.name, "A")


class ObserverTests(unittest.TestCase):
    def test_email_sent_through_mock_sender(self):
        sender = Mock()
        bus = EventBus()
        bus.subscribe("registered", EmailNotifier(sender).on_registered)
        bus.publish("registered", {"email": "a@b.c", "name": "A",
                                   "event_title": "T", "amount": 10})
        sender.send.assert_called_once()
        self.assertEqual(sender.send.call_args.kwargs["to"], "a@b.c")

    def test_publish_without_subscribers_is_safe(self):
        EventBus().publish("nothing", {})

class ConsoleSenderTests(unittest.TestCase):
    def test_console_sender_prints(self):
        import io
        from contextlib import redirect_stdout
        from app.notifications import ConsoleSender
        buf = io.StringIO()
        with redirect_stdout(buf):
            ConsoleSender().send("a@b.c", "Hi", "Body")
        self.assertIn("a@b.c", buf.getvalue())