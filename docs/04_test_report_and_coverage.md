# 3. Test report
Run: `pytest --cov=app --cov-report=term-missing` and paste the table + screenshot of green CI here.

| Area | Technique | File |
|---|---|---|
| Factory, Strategy | TDD unit tests | tests/test_factory.py, test_pricing.py |
| Registration/User services | Mocks for repository, gateway, bus | tests/test_registration_service.py |
| Adapter | Mocked vendor client | tests/test_payment_adapter.py |
| REST + UI + OpenAPI sync | Integration (Flask test client) | tests/test_api.py |
| UI | Selenium (headless Chrome, in CI) | tests/test_e2e_selenium.py |

Baseline in my environment: 42 tests, all passing (2 Selenium tests need Chrome and run in CI). Paste your real coverage % after running locally.
