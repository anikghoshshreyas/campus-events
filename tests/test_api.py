"""Integration tests through the Flask test client (in-memory SQLite)."""
import os
import unittest
from unittest.mock import Mock
from app import create_app
from app.payment import PaymentResult
import yaml


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.gateway = Mock()
        self.gateway.pay.return_value = PaymentResult(True, "R")
        self.sender = Mock()
        self.app = create_app(":memory:", gateway=self.gateway, sender=self.sender)
        self.c = self.app.test_client()

    def _user(self, email="a@b.c", role="student"):
        return self.c.post("/api/users", json={"name": "A", "email": email, "role": role})

    def _event(self, kind="workshop", cap=1):
        return self.c.post("/api/events", json={
            "kind": kind, "title": "Git", "date": "2099-01-01", "capacity": cap})

    def test_full_registration_flow(self):
        uid = self._user().get_json()["id"]
        eid = self._event().get_json()["id"]
        r = self.c.post(f"/api/events/{eid}/register", json={"user_id": uid})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.get_json()["amount_paid"], 160.0)
        self.sender.send.assert_called_once()
        regs = self.c.get(f"/api/events/{eid}/registrations").get_json()
        self.assertEqual(len(regs), 1)

    def test_event_becomes_full(self):
        u1 = self._user("a@b.c").get_json()["id"]
        u2 = self._user("d@e.f").get_json()["id"]
        eid = self._event(cap=1).get_json()["id"]
        self.c.post(f"/api/events/{eid}/register", json={"user_id": u1})
        r = self.c.post(f"/api/events/{eid}/register", json={"user_id": u2})
        self.assertEqual(r.status_code, 409)

    def test_duplicate_email_409(self):
        self._user()
        self.assertEqual(self._user().status_code, 409)

    def test_bad_event_400(self):
        r = self.c.post("/api/events", json={"kind": "x", "title": "t", "date": "2099-01-01"})
        self.assertEqual(r.status_code, 400)

    def test_lists(self):
        self._user(); self._event()
        self.assertEqual(len(self.c.get("/api/users").get_json()), 1)
        self.assertEqual(len(self.c.get("/api/events").get_json()), 1)

    def test_index_page_and_ui_create(self):
        self.assertEqual(self.c.get("/").status_code, 200)
        r = self.c.post("/ui/events", data={"title": "T", "kind": "seminar", "date": "2099-01-01"})
        self.assertEqual(r.status_code, 302)
        self.assertIn(b"T (seminar", self.c.get("/").data)

    def test_ui_create_error_shown(self):
        r = self.c.post("/ui/events", data={"title": "", "kind": "seminar", "date": "2099-01-01"},
                        follow_redirects=True)
        self.assertIn(b"Title is required", r.data)

    def test_docs_and_spec_served(self):
        self.assertEqual(self.c.get("/docs").status_code, 200)
        self.assertEqual(self.c.get("/openapi.yaml").status_code, 200)

    def test_every_api_route_is_documented_in_openapi(self):
        """New-tool evidence: the OpenAPI spec must stay in sync with the code."""
        path = os.path.join(os.path.dirname(__file__), "..", "openapi.yaml")
        with open(path, encoding="utf-8") as fh:
            spec = yaml.safe_load(fh)
        documented = {(p, m.upper()) for p, ops in spec["paths"].items() for m in ops}
        actual = set()
        for rule in self.app.url_map.iter_rules():
            if rule.rule.startswith("/api/"):
                p = rule.rule.replace("<int:event_id>", "{event_id}")
                for m in rule.methods - {"HEAD", "OPTIONS"}:
                    actual.add((p, m))
        self.assertEqual(actual, documented)
