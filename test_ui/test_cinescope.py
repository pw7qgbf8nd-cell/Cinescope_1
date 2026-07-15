from playwright.sync_api import sync_playwright
import time
import pytest
import allure
from pages.register_page import CinescopRegisterPage
from pages.login_page import CinescopLoginPage
from pages.main_page import CinescopMainPage
from pages.film_page import CinescopFilmPage
from pages.action_page import PageAction
from utils import DataGenerator

@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Login")
@pytest.mark.ui
class TestloginPage:
    @allure.title("Проведение успешного входа в систему")
    def test_login_by_ui(self, registered_user):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=False)
            page = browser.new_page()
            login_page = CinescopLoginPage(page)
            with allure.step("Открытие страницы авторизации"):
                login_page.open()
                with allure.step("авторизация пользователя, автоматическое заполнение данных"):
                    login_page.login(registered_user.email, registered_user.password)
                    with allure.step("Проверка редиректа на главную страницу проекта"):
                        login_page.assert_was_redirect_to_home_page()
                        with allure.step("Создание скриншота в следствии доказательства работы сервиса"):
                            login_page.make_screenshot_and_attach_to_allure()
                            with allure.step("Закрытие браузера"):
                                browser.close()


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Register")
@pytest.mark.ui
class TestRegisterPage:
    @allure.title("Проведение успешной регистрации")
    def test_register_by_ui(self, new_user):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()
            register_page = CinescopRegisterPage(page)
            with allure.step("Открытие страницы регистрации"):
                register_page.open()
                with allure.step("регистрация пользователя, автоматическое заполнение данных"):
                    register_page.register(new_user.full_name, new_user.email, new_user.password, new_user.password)
                    with allure.step("Проверка редиректа на страницу авторизации проекта"):
                        register_page.assert_was_redirect_to_login_page()
                        with allure.step("Проверка появления POP UP элемента с написью 'вы успешно зарегестрировались'"):
                            register_page.assert_allert_was_pop_up()
                            with allure.step("Закрытие браузера"):
                                browser.close()

@allure.epic("Тестирование UI")
@allure.feature("Тестирование страницы фильма")
@pytest.mark.ui
class TestFilmPage:
    @allure.title("Создание отзыва")
    def test_feedback_film(self, registered_user):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()
            login_page = CinescopLoginPage(page)
            with allure.step("Открытие страницы авторизации"):
                login_page.open()
                with allure.step("авторизация пользователя, автоматическое заполнение данных"):
                    login_page.login(registered_user.email, registered_user.password)
                    with allure.step("Проверка редиректа на главную страницу проекта"):
                        login_page.wait_redirect_for_url("https://dev-cinescope.coconutqa.ru/")
                        with allure.step("Создания главной страницы"):
                            main_page = CinescopMainPage(page)
                            with allure.step("Открие первого по локатору фильма"):
                                main_page.open_first_movies()
                                with allure.step("Проверка перехода на страницу фильма"):
                                    main_page.assert_was_redirect_to_film_page()
                                    with allure.step("Создание шаблона страницы фильма"):
                                        film_page = CinescopFilmPage(page)
                                        with allure.step("Автозаполнение поля отзыва и его публикация"):
                                            film_page.write_and_confirm_feedback(registered_user.feedback)
                                            with allure.step("Проверка появления POP UP элемента с написью 'отзыв успешно опубликован'"):
                                                film_page.assert_allert_was_pop_up_feedback()
                                                with allure.step("Проверка что написанный отзыв и опубликованный отзыв на странице фильма по локатору одинковы"):
                                                    film_page.assert_review_was_published_and_equal_written(registered_user.feedback)
                                                    with allure.step("Создание скриншота в следствии доказательства работы сервиса"):
                                                        film_page.make_screenshot_and_attach_to_allure()
                                                        with allure.step("Удаление отзыва после его публкации и проверки, чтобы почистить за собой и сделать тест воспроизводимым"):
                                                            film_page.delete_feedback()
                                                            with allure.step("Закрытие браузера"):
                                                                browser.close()

