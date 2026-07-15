from playwright.sync_api import Page, expect
import pytest
from playwright.sync_api import sync_playwright
import allure
from pages.base_page import BasePage

class CinescopMainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = self.home_url
        self.detailes_of_film_button = 'xpath=/html/body/div[2]/main/div[1]/div[1]/div[3]/a/button'

    @allure.step("Открытие первого фильма в списке")
    def open_first_movies(self):
        self.page.click(self.detailes_of_film_button)

    @allure.step("Проверка перехода по ссылке к определенному фильму")
    def assert_was_redirect_to_film_page(self):
        self.wait_redirect_for_url("https://dev-cinescope.coconutqa.ru/movies/57747")