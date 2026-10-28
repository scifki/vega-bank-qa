from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parent.parent
out = root / "screenshots"
SCALE = 2
URL = "https://scifki.github.io/vega-bank-qa/"

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    ctx = browser.new_context(
        viewport={"width": 960, "height": 1100},
        device_scale_factor=SCALE,
        locale="ru-RU",
    )
    page = ctx.new_page()
    page.goto(URL, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    tmp = out / "_pages_full.png"
    page.screenshot(path=str(tmp), full_page=True)
    with Image.open(tmp) as im:
        print("full:", im.size, flush=True)
        w, h = im.size
        top = min(760 * SCALE, h)
        im.crop((0, 0, w, top)).save(out / "gh_report.png")
        start = min(700 * SCALE, max(0, h - 900 * SCALE))
        im.crop((0, start, w, min(h, start + 1000 * SCALE))).save(out / "gh_report_steps.png")
    tmp.unlink()
    browser.close()
    for n in ("gh_report.png", "gh_report_steps.png"):
        with Image.open(out / n) as im:
            print(n, im.size)
