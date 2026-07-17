from playwright.sync_api import Page, expect, sync_playwright
from pages.action_page import PageAction


class BasePage(PageAction): #Базовая логика доспустимая для всех страниц на сайте
    def __init__(self, page: Page):
        super().__init__(page)
        self.home_url = "https://dev-cinescope.coconutqa.ru/"

