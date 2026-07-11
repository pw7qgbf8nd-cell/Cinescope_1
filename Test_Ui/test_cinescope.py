import email

from playwright.sync_api import Page, expect
import time
import pytest
from random import randint
from pathlib import Path
from datetime import datetime
import os
from playwright.sync_api import sync_playwright
import allure
from Test_Ui.cinescope_classes import CinescopRegisterPage, CinescopLoginPage , CinescopMainPage , CinescopFilmPage
import random
import random
import string
from faker import Faker
import datetime
from Utils import DataGenerator
import time
from playwright.sync_api import sync_playwright

@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Login")
@pytest.mark.ui
class TestloginPage:
    @allure.title("Проведение успешного входа в систему")
    def test_login_by_ui(self    ):
        with sync_playwright() as playwright:
            email = "test223@email.qa"
            password = "OLEG_AQA25"
            browser = playwright.chromium.launch(
                headless=False)  # Запуск браузера headless=False для визуального отображения
            page = browser.new_page()
            login_page = CinescopLoginPage(page)  # Создаем объект страницы Login

            login_page.open()
            login_page.login(email, password)  # Осуществяем вход

            login_page.assert_was_redirect_to_home_page()  # Проверка редиректа на домашнюю страницу
            login_page.make_screenshot_and_attach_to_allure()  # Прикрепляем скриншот
            login_page.assert_allert_was_pop_up()  # Проверка появления и исчезновения алерта

            # Пауза для визуальной проверки (нужно удалить в реальном тестировании)
            time.sleep(5)
            browser.close()


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Register")
@pytest.mark.ui
class TestRegisterPage:
    @allure.title("Проведение успешной регистрации")
    def test_register_by_ui(self):
        with sync_playwright() as playwright:
            # Подготовка данных для регистрации
            random_email = DataGenerator.generate_random_email()
            random_name = DataGenerator.generate_random_name()
            random_password = DataGenerator.generate_random_password()

            browser = playwright.chromium.launch(
                headless=False)  # Запуск браузера headless=False для визуального отображения
            page = browser.new_page()

            register_page = CinescopRegisterPage(page)  # Создаем объект страницы регистрации cinescope
            register_page.open()
            register_page.register(f"PlaywrightTest {random_name}", random_email, random_password,
                                   random_password)  # Выполняем регистрацию

            register_page.assert_was_redirect_to_login_page()  # Проверка редиректа на страницу /login
            # register_page.make_screenshot_and_attach_to_allure()  # Прикрепляем скриншот
            register_page.assert_allert_was_pop_up()  # Проверка появления и исчезновения алерта

            # Пауза для визуальной проверки (нужно удалить в реальном тестировании)
            time.sleep(5)
            browser.close()

@allure.epic("Тестирование UI")
@allure.feature("Тестирование страницы фильма")
@pytest.mark.ui
class TestFilmPage:
    @allure.title("Создание отзыва")
    def test_feedback_film(self):
        with sync_playwright() as playwright:
            # Подготовка данных для авторизации и оставления отызва
            email = "test223@email.qa"
            password = "OLEG_AQA25"
            feedback = "Под пиво пойдет"

            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()
            login_page = CinescopLoginPage(page)
            login_page.open()
            login_page.login(email, password)
            login_page.assert_allert_was_pop_up()
            login_page.reload_page()
            login_page.wait_redirect_for_url("https://dev-cinescope.coconutqa.ru/")
            # login_page.make_screenshot_and_attach_to_allure()
            main_page = CinescopMainPage(page)
            main_page.open_url("https://dev-cinescope.coconutqa.ru/")
            main_page.open_movies()
            main_page.assert_was_redirect_to_film_page()
            film_page = CinescopFilmPage(page)
            film_page.write_and_confirm_feedback(feedback)
            film_page.assert_allert_was_pop_up_feedback()
            time.sleep(5)
            browser.close()

