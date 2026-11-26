import os
from flask import Blueprint, current_app, jsonify, request, render_template, redirect, url_for
from .models import DomainError

bp = Blueprint("main", __name__)


def svc(name):
    return current_app.extensions["services"][name]


@bp.app_errorhandler(DomainError)
def handle_domain_error(err):
    return jsonify(error=str(err)), err.status


@bp.get("/api/users")
def list_users():
    return jsonify([u.to_dict() for u in svc("users").users.all()])


@bp.post("/api/users")
def create_user():
    d = request.get_json(force=True, silent=True) or {}
    u = svc("users").create(d.get("name"), d.get("email"), d.get("role", "student"))
    return jsonify(u.to_dict()), 201


@bp.get("/api/events")
def list_events():
    return jsonify([e.to_dict() for e in svc("events").events.all()])


@bp.post("/api/events")
def create_event():
    d = request.get_json(force=True, silent=True) or {}
    e = svc("events").create(d.get("kind"), d.get("title"), d.get("date"),
                             d.get("capacity"), d.get("fee"))
    return jsonify(e.to_dict()), 201


@bp.post("/api/events/<int:event_id>/register")
def register(event_id):
    d = request.get_json(force=True, silent=True) or {}
    r = svc("registrations").register(d.get("user_id"), event_id)
    return jsonify(r.to_dict()), 201


@bp.get("/api/events/<int:event_id>/registrations")
def event_registrations(event_id):
    return jsonify([r.to_dict() for r in svc("registrations").regs.for_event(event_id)])


# ---- simple web UI (used by the Selenium test) ----
@bp.get("/")
def index():
    return render_template("index.html", events=svc("events").events.all(),
                           error=request.args.get("error"))


@bp.post("/ui/events")
def ui_create_event():
    f = request.form
    try:
        svc("events").create(f.get("kind"), f.get("title"), f.get("date"),
                             f.get("capacity") or None)
    except DomainError as e:
        return redirect(url_for("main.index", error=str(e)))
    return redirect(url_for("main.index"))


# ---- OpenAPI / Swagger UI (the new tool learned) ----
@bp.get("/openapi.yaml")
def openapi_spec():
    path = os.path.join(os.path.dirname(__file__), "..", "openapi.yaml")
    with open(path, encoding="utf-8") as fh:
        return fh.read(), 200, {"Content-Type": "text/yaml"}


@bp.get("/docs")
def docs():
    return """<!doctype html><html><head><title>API Docs</title>
<link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css"></head>
<body><div id="ui"></div>
<script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
<script>SwaggerUIBundle({url:'/openapi.yaml',dom_id:'#ui'})</script></body></html>"""
