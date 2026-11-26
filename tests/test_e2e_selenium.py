"""End-to-end UI test with Selenium. Skipped automatically if Selenium or
Chrome is unavailable (it runs in the GitHub Actions CI)."""
import threading
import unittest

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    HAVE_SELENIUM = True
except ImportError:  # pragma: no cover
    HAVE_SELENIUM = False

from werkzeug.serving import make_server
from app import create_app


@unittest.skipUnless(HAVE_SELENIUM, "selenium not installed")
class UiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        opts = Options()
        for a in ("--headless=new", "--no-sandbox", "--disable-dev-shm-usage"):
            opts.add_argument(a)
        try:
            cls.driver = webdriver.Chrome(options=opts)
        except Exception as exc:  # no browser on this machine
            raise unittest.SkipTest(f"Chrome not available: {exc}")
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.server = make_server("127.0.0.1", 5055, create_app(":memory:"))
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "driver"):
            cls.driver.quit()
            cls.server.shutdown()

    def test_create_event_through_form(self):
        d = self.driver
        d.get("http://127.0.0.1:5055/")
        self.assertEqual(d.find_element(By.ID, "heading").text, "Campus Events")
        d.find_element(By.ID, "title").send_keys("Selenium Workshop")
        d.find_element(By.ID, "date").send_keys("2099-05-05")
        d.find_element(By.ID, "capacity").send_keys("20")
        d.find_element(By.ID, "kind").send_keys("workshop")
        d.find_element(By.ID, "submit").click()
        # wait for the redirect + reload before reading the list
        self.wait.until(EC.text_to_be_present_in_element(
            (By.ID, "event-list"), "Selenium Workshop"))
        items = [e.text for e in d.find_elements(By.CLASS_NAME, "event")]
        self.assertTrue(any("Selenium Workshop" in t for t in items))

    def test_invalid_event_shows_error(self):
        d = self.driver
        d.get("http://127.0.0.1:5055/")
        d.find_element(By.ID, "date").send_keys("bad")
        d.find_element(By.ID, "submit").click()
        error = self.wait.until(EC.presence_of_element_located((By.ID, "error")))
        self.assertIn("Title is required", error.text)