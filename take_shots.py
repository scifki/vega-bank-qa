import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

root = Path(__file__).parent
shots = root / "screenshots"
shots.mkdir(exist_ok=True)
report = root / "allure-report"

# Отчёт Allure подгружает данные через fetch, поэтому открываем его по HTTP.
server = subprocess.Popen(
    [sys.executable, "-m", "http.server", "8765", "--bind", "127.0.0.1"],
    cwd=report,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
time.sleep(2)

try:
    with sync_playwright() as pw:
        pw.selectors.set_test_id_attribute("data-test-id")
        browser = pw.chromium.launch()

        # 1-2. Форма: успешный перевод и ошибка
        page = browser.new_page(viewport={"width": 900, "height": 700})
        for amount, name in (("500", "form_success"), ("20000", "form_error")):
            page.goto((root / "transfer.html").resolve().as_uri())
            page.get_by_test_id("transfer-amount").fill(amount)
            page.get_by_test_id("transfer-submit").click()
            box = page.locator("body").bounding_box()
            page.screenshot(
                path=str(shots / f"{name}.png"),
                clip={"x": 0, "y": 0, "width": 900, "height": max(200, box["height"] + 40)},
            )

        # 3-5. Отчёт Allure
        page = browser.new_page(viewport={"width": 1400, "height": 950})
        page.goto("http://127.0.0.1:8765/index.html")
        page.wait_for_selector("text=Перевод между своими счетами", timeout=30000)
        page.wait_for_timeout(2000)
        page.screenshot(path=str(shots / "allure_overview.png"))

        page.goto("http://127.0.0.1:8765/index.html#suites")
        page.wait_for_selector("text=Успешный перевод", timeout=30000)
        page.wait_for_timeout(2000)
        page.screenshot(path=str(shots / "allure_suites.png"))

        page.get_by_text("Недостаточно средств", exact=True).first.click()
        page.wait_for_timeout(2500)
        page.screenshot(path=str(shots / "allure_test_steps.png"))

        browser.close()
finally:
    server.terminate()

print("screenshots ok")
