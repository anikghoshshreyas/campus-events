"""Business logic. All dependencies are injected so tests can mock them."""
from .models import User, Registration, DomainError
from .factory import EventFactory
from .pricing import choose_strategy

ROLES = {"student", "staff", "guest"}


class UserService:
    def __init__(self, users):
        self.users = users

    def create(self, name, email, role="student"):
        if not name or "@" not in (email or ""):
            raise DomainError("Valid name and email are required")
        if role not in ROLES:
            raise DomainError("Invalid role")
        if self.users.by_email(email):
            raise DomainError("Email already registered", 409)
        return self.users.add(User(None, name.strip(), email.strip(), role))


class EventService:
    def __init__(self, events):
        self.events = events

    def create(self, kind, title, event_date, capacity=None, fee=None):
        return self.events.add(EventFactory.create(kind, title, event_date, capacity, fee))


class RegistrationService:
    def __init__(self, users, events, regs, gateway, bus, today=None):
        self.users, self.events, self.regs = users, events, regs
        self.gateway, self.bus, self.today = gateway, bus, today

    def register(self, user_id, event_id):
        user = self.users.get(user_id)
        event = self.events.get(event_id)
        if not user or not event:
            raise DomainError("User or event not found", 404)
        if self.regs.exists(user_id, event_id):
            raise DomainError("Already registered", 409)
        if self.regs.count_for_event(event_id) >= event.capacity:
            raise DomainError("Event is full", 409)

        amount = choose_strategy(user.role, event.date, self.today).price(event.base_fee)
        if amount > 0:
            result = self.gateway.pay(amount, user.email)
            if not result.success:
                raise DomainError("Payment failed", 402)

        reg = self.regs.add(Registration(None, user_id, event_id, amount))
        self.bus.publish("registered", {
            "email": user.email, "name": user.name,
            "event_title": event.title, "amount": amount})
        return reg
