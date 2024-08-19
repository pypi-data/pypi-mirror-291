import re
from playwright.sync_api import Page, expect


def test_has_title(page: Page):
    page.goto("localhost:8501")

    free_text_select = page.get_by_role("searchbox")
    print(free_text_select.inner_html())

    assert False
