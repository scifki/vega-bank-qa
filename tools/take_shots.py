import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parent.parent
shots = root / "screenshots"
shots.mkdir(exist_ok=True)
report = root / "reports" / "behave-report.html"

# Отчёт пересобираем, чтобы скриншоты совпадали с текущими тестами.
subprocess.run([sys.executable, "-m", "behave", "-f", "json", "-o", "reports/behave.json", "features"],
               cwd=root, check=True, stdout=subprocess.DEVNULL)
subprocess.run([sys.executable, "make_html_report.py", "reports/behave.json", "reports/behave-report.html"],
               cwd=root, check=True)

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

    # 3-4. HTML-отчёт
    page = browser.new_page(viewport={"width": 1100, "height": 900})
    page.goto(report.resolve().as_uri())
    page.wait_for_timeout(700)
    page.screenshot(path=str(shots / "report_overview.png"))

    # 4. Отчёт с раскрытыми шагами всех сценариев
    page.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
    page.wait_for_timeout(400)
    page.screenshot(path=str(shots / "report_steps.png"), full_page=True)

    browser.close()

print("screenshots ok")

