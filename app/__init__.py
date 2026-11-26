from flask import Flask
from .repositories import Database, UserRepository, EventRepository, RegistrationRepository
from .services import UserService, EventService, RegistrationService
from .payment import VendorGatewayAdapter, LegacyVendorClient
from .notifications import EventBus, EmailNotifier, ConsoleSender
from .routes import bp


def create_app(db_path="campus.db", gateway=None, sender=None):
    app = Flask(__name__)
    db = Database(db_path)
    users, events, regs = UserRepository(db), EventRepository(db), RegistrationRepository(db)
    gateway = gateway or VendorGatewayAdapter(LegacyVendorClient())
    bus = EventBus()
    bus.subscribe("registered", EmailNotifier(sender or ConsoleSender()).on_registered)
    app.extensions["services"] = {
        "users": UserService(users),
        "events": EventService(events),
        "registrations": RegistrationService(users, events, regs, gateway, bus),
    }
    app.register_blueprint(bp)
    return app
