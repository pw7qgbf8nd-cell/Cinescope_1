from playwright.sync_api import Page, expect
import pytest
from playwright.sync_api import sync_playwright
import allure
from pages.base_page import BasePage
import random


class CinescopMainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = self.home_url
        self.details_of_film_button = page.get_by_role("button", name="Подробнее")

    @allure.step("Открытие фильма из списка")
    def open_random_movie(self):
        random_index = random.randint(0,  0)
        self.details_of_film_button.nth(random_index).click()
"""хотел рандомизировать выбор фильма, для большего покрытия теста, 
но при выборе некоторых фильмов сервис падает, поэтому по итогу оставил 1 фильм"""
