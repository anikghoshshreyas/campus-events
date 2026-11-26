"""Plain data classes shared by all modules."""
from dataclasses import dataclass, asdict


@dataclass
class User:
    id: int | None
    name: str
    email: str
    role: str = "student"  # student | staff | guest

    def to_dict(self):
        return asdict(self)


@dataclass
class Event:
    id: int | None
    title: str
    date: str  # ISO date: YYYY-MM-DD
    capacity: int
    base_fee: float
    kind: str

    def to_dict(self):
        return asdict(self)


@dataclass
class Registration:
    id: int | None
    user_id: int
    event_id: int
    amount_paid: float

    def to_dict(self):
        return asdict(self)


class DomainError(Exception):
    """Business-rule violation; routes translate it to an HTTP error."""

    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status
