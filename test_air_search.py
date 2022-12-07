import re
from playwright.sync_api import Page, expect
import pytest_check as check
from faker import Faker
import pytest

fake = Faker()


@pytest.mark.parametrize('local',
                         [".co.uk", pytest.param(".com", marks=pytest.mark.skip(reason="Just for example")), ".ae"])
def test_air_search(page: Page, local):
    page.goto(f"https://flyxo{local}")

    where_from = page.get_by_placeholder("Where from?")
    where_to = page.get_by_placeholder("Where to?")

    where_from.click()
    page.get_by_text("UDYZ, Yerevan").click()
    expect(where_from).to_have_value("Zvartnots Intl")

    where_to.fill("Lisbon")
    page.get_by_text("LPPT, Lisbon (Lisboa)").click()
    expect(where_to).to_have_value("Humberto Delgado")

    page.get_by_role("button", name="Search").click()
    expect(page).to_have_url(re.compile(".*search"))
    #    check.is_in("search", page.url)

    page.locator("button:nth-child(5)").click()
    expect(page.locator("div._Dg > button")).to_have_text("Heavy")

    page.locator("button._CT._ET").click()
    expect(page.get_by_role("dialog")).to_be_visible()

    page.locator("#field-email").fill(fake.email())
    page.locator("#field-password").fill(fake.password())
    page.locator(".login__button").click()
    expect(page.locator(".field__error")).to_have_text(re.compile(".*Please try again"))
