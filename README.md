# Campus Event Manager (CSE 3206 – CO4 project)

Create events, register students/staff, apply pricing rules, charge payments and
send notifications. Flask + SQLite.

## Modules
1. User management  2. Event management  3. Registration  4. Payment (Adapter)  5. Notifications (Observer)  6. Pricing (Strategy)

## Run
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py            # UI: http://127.0.0.1:5000/   API docs: http://127.0.0.1:5000/docs
pytest --cov=app --cov-report=term-missing
```

## Design patterns
| Pattern | Category | File |
|---|---|---|
| Factory Method | Creational | app/factory.py |
| Adapter | Structural | app/payment.py |
| Strategy | Behavioral | app/pricing.py |
| Observer | Behavioral | app/notifications.py |

## New tool learned: OpenAPI / Swagger
`openapi.yaml` documents the API; Swagger UI is served at `/docs`; a test fails if a route is undocumented.

## Git workflow
Branches: `feature/<topic>`, `fix/<topic>`, `docs/<topic>`. Commits: `type(scope): message` (feat, fix, test, docs, ci, refactor). All changes go through pull requests into `main`.

## AI usage statement
(Write honestly which parts AI helped with and that you can explain every part.)
