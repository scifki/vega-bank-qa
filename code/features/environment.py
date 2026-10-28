from pathlib import Path

from playwright.sync_api import sync_playwright


def before_all(context):
    context.page_url = Path("transfer.html").resolve().as_uri()
    context.playwright = sync_playwright().start()
    context.playwright.selectors.set_test_id_attribute("data-test-id")
    context.browser = context.playwright.chromium.launch()


def before_scenario(context, scenario):
    context.page = context.browser.new_page()


def after_scenario(context, scenario):
    context.page.close()


def after_all(context):
    context.browser.close()
    context.playwright.stop()
