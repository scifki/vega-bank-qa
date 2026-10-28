from behave import given, when, then
from playwright.sync_api import expect


@given("пользователь открыл форму перевода")
def step_open_form(context):
    context.page.goto(context.page_url)


@when("пользователь выбирает счёт списания «{account}»")
def step_choose_source(context, account):
    context.page.get_by_test_id("transfer-source").select_option(label=account)


@when("пользователь выбирает счёт зачисления «{account}»")
def step_choose_target(context, account):
    context.page.get_by_test_id("transfer-target").select_option(label=account)


@when("вводит сумму {amount}")
def step_enter_amount(context, amount):
    context.page.get_by_test_id("transfer-amount").fill(amount)


@when("нажимает кнопку «Перевести»")
def step_click_submit(context):
    context.page.get_by_test_id("transfer-submit").click()


@then("на экране отображается сообщение «{text}»")
def step_check_message(context, text):
    expect(context.page.get_by_test_id("transfer-message")).to_have_text(text)
