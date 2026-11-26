"""SQLite persistence (the external dependency that tests mock)."""
import sqlite3
from .models import User, Event, Registration

SCHEMA = """
CREATE TABLE IF NOT EXISTS users(
  id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE, role TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS events(
  id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, date TEXT NOT NULL,
  capacity INTEGER NOT NULL, base_fee REAL NOT NULL, kind TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS registrations(
  id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
  event_id INTEGER NOT NULL, amount_paid REAL NOT NULL,
  UNIQUE(user_id, event_id));
"""


class Database:
    def __init__(self, path="campus.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()


class UserRepository:
    def __init__(self, db):
        self.db = db

    def add(self, u: User) -> User:
        cur = self.db.conn.execute(
            "INSERT INTO users(name,email,role) VALUES(?,?,?)",
            (u.name, u.email, u.role))
        self.db.conn.commit()
        u.id = cur.lastrowid
        return u

    def get(self, uid):
        r = self.db.conn.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
        return User(**dict(r)) if r else None

    def by_email(self, email):
        r = self.db.conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        return User(**dict(r)) if r else None

    def all(self):
        return [User(**dict(r)) for r in self.db.conn.execute("SELECT * FROM users")]


class EventRepository:
    def __init__(self, db):
        self.db = db

    def add(self, e: Event) -> Event:
        cur = self.db.conn.execute(
            "INSERT INTO events(title,date,capacity,base_fee,kind) VALUES(?,?,?,?,?)",
            (e.title, e.date, e.capacity, e.base_fee, e.kind))
        self.db.conn.commit()
        e.id = cur.lastrowid
        return e

    def get(self, eid):
        r = self.db.conn.execute("SELECT * FROM events WHERE id=?", (eid,)).fetchone()
        return Event(**dict(r)) if r else None

    def all(self):
        return [Event(**dict(r)) for r in self.db.conn.execute("SELECT * FROM events ORDER BY date")]


class RegistrationRepository:
    def __init__(self, db):
        self.db = db

    def add(self, r: Registration) -> Registration:
        cur = self.db.conn.execute(
            "INSERT INTO registrations(user_id,event_id,amount_paid) VALUES(?,?,?)",
            (r.user_id, r.event_id, r.amount_paid))
        self.db.conn.commit()
        r.id = cur.lastrowid
        return r

    def exists(self, user_id, event_id):
        return self.db.conn.execute(
            "SELECT 1 FROM registrations WHERE user_id=? AND event_id=?",
            (user_id, event_id)).fetchone() is not None

    def count_for_event(self, event_id):
        return self.db.conn.execute(
            "SELECT COUNT(*) FROM registrations WHERE event_id=?", (event_id,)).fetchone()[0]

    def for_event(self, event_id):
        return [Registration(**dict(r)) for r in self.db.conn.execute(
            "SELECT * FROM registrations WHERE event_id=?", (event_id,))]
