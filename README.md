# Campus Event Manager

**Student:** Anik Ghosh | **Roll:** 2203017 | CSE 3206 Software Engineering Sessional (22 Series), RUET

A web app and REST API for creating campus events, registering students and staff, applying pricing rules, taking payments and sending confirmation e-mails. Built with Flask and SQLite following the full SDLC.

## Modules

1. User management 2. Event management 3. Registration 4. Payment (Adapter) 5. Notifications (Observer) 6. Pricing (Strategy)

## Run it

    python -m venv .venv
    .venv\Scripts\activate        (Linux/Mac: source .venv/bin/activate)
    pip install -r requirements.txt
    python run.py

- App: http://127.0.0.1:5000/
- API docs (Swagger): http://127.0.0.1:5000/docs

## Run the tests

    pytest --cov=app --cov-report=term-missing

## Design patterns

| Pattern        | Category   | File                 |
| -------------- | ---------- | -------------------- |
| Factory Method | Creational | app/factory.py       |
| Adapter        | Structural | app/payment.py       |
| Strategy       | Behavioral | app/pricing.py       |
| Observer       | Behavioral | app/notifications.py |

## New tool learned: OpenAPI / Swagger

openapi.yaml describes the API, Swagger UI is served at /docs, and a test fails if an endpoint is not documented.

## Git workflow

Branches: feature/<topic>, fix/<topic>, docs/<topic>. Commits: type(scope): message. All changes go through pull requests into main, and CI runs on every push.

## AI usage statement

[Write this yourself, honestly. For example: "Claude (Anthropic) generated the starter project structure, tests and documentation templates. I ran, tested and modified it, wrote [list what you wrote], and I can explain every part."]
