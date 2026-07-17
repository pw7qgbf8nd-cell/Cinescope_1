from playwright.sync_api import Page, expect
import pytest
from playwright.sync_api import sync_playwright
import allure
from pages.base_page import BasePage

class CinescopLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}login"
        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"
        self.login_button = "button[data-qa-id='login_submit_button']"


    def open(self):
        self.open_url(self.url)

    @allure.step("Заполнения полей для авторизации")
    def login(self, email: str, password: str):
        self.enter_text_to_element(self.password_input, password)
        self.enter_text_to_element(self.email_input, email)
        self.click_element(self.login_button)

    @allure.step("Проверка возвращения на домашнюю страницу")
    def assert_was_redirect_to_home_page(self):
        self.wait_redirect_for_url(self.home_url)

    @allure.step(" POP UP окно с уведомлением")
    def assert_allert_was_pop_up(self):
        self.check_pop_up_element_with_text("Вы вошли в аккаунт")