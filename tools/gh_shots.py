import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parent.parent
out = root / "screenshots"
out.mkdir(exist_ok=True)

REPO = "https://github.com/scifki/vega-bank-qa"
SCALE = 2
MAX_H = 1000  # CSS-пикселей по высоте, лишнее обрезаем

TARGETS = {
    "repo": ("gh_repo.png", REPO),
    "feature": ("gh_feature.png", f"{REPO}/blob/main/features/transfer.feature"),
    "steps": ("gh_steps.png", f"{REPO}/blob/main/features/steps/transfer_steps.py"),
    "db": ("gh_db.png", f"{REPO}/blob/main/db_check.py"),
    "actions": ("gh_actions.png", f"{REPO}/actions"),
    "run": ("gh_actions.png", f"{REPO}/actions/runs/40699352386"),
}

keys = sys.argv[1:] or list(TARGETS)

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    ctx = browser.new_context(
        viewport={"width": 960, "height": 1100},
        device_scale_factor=SCALE,
        locale="ru-RU",
    )
    ctx.set_default_timeout(15000)
    ctx.set_default_navigation_timeout(25000)
    page = ctx.new_page()
    for key in keys:
        name, url = TARGETS[key]
        path = out / name
        try:
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)
            title = page.title()
            if "Page not found" in title:
                print(key, "FAIL: 404", flush=True)
                continue
            page.locator("main").first.screenshot(path=str(path))
            with Image.open(path) as im:
                if im.height > MAX_H * SCALE:
                    im.crop((0, 0, im.width, MAX_H * SCALE)).save(path)
            with Image.open(path) as im:
                print(key, name, im.size, flush=True)
        except Exception as exc:
            print(key, "ERROR", type(exc).__name__, str(exc).splitlines()[0][:120], flush=True)
    browser.close()
