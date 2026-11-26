"""Creational pattern: Factory Method for events.

Problem: each kind of event has different default fee/capacity rules.
Rejected alternative: a big if/elif inside the route handler (hard to extend,
hard to test)."""
from datetime import date
from .models import Event, DomainError

# kind -> (default fee, max capacity)
EVENT_KINDS = {
    "seminar": (0.0, 300),
    "workshop": (250.0, 50),
    "concert": (500.0, 1000),
}


class EventFactory:
    @staticmethod
    def create(kind, title, event_date, capacity=None, fee=None):
        if kind not in EVENT_KINDS:
            raise DomainError(f"Unknown event kind: {kind}")
        if not title or not title.strip():
            raise DomainError("Title is required")
        try:
            date.fromisoformat(event_date)
        except (TypeError, ValueError):
            raise DomainError("Date must be YYYY-MM-DD")
        default_fee, max_cap = EVENT_KINDS[kind]
        capacity = max_cap if capacity is None else int(capacity)
        if capacity <= 0 or capacity > max_cap:
            raise DomainError(f"Capacity for {kind} must be 1..{max_cap}")
        fee = default_fee if fee is None else float(fee)
        if fee < 0:
            raise DomainError("Fee cannot be negative")
        return Event(None, title.strip(), event_date, capacity, fee, kind)
