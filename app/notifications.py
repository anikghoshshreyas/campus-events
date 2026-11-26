"""Behavioral pattern: Observer for notifications.

Problem: registration should trigger e-mail/log/etc. without the service
knowing who listens. Rejected alternative: calling the mailer directly."""


class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, topic, callback):
        self._subscribers.setdefault(topic, []).append(callback)

    def publish(self, topic, payload):
        for cb in self._subscribers.get(topic, []):
            cb(payload)


class EmailNotifier:
    """sender is injected (SMTP in production, a Mock in tests)."""

    def __init__(self, sender):
        self.sender = sender

    def on_registered(self, payload):
        self.sender.send(
            to=payload["email"],
            subject=f"Registered: {payload['event_title']}",
            body=f"Hi {payload['name']}, you paid {payload['amount']:.2f}.",
        )


class ConsoleSender:
    def send(self, to, subject, body):
        print(f"[EMAIL] to={to} subject={subject} body={body}")
