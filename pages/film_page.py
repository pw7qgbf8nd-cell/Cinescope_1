from playwright.sync_api import Page, expect, sync_playwright
import allure
from pages.base_page import BasePage

class CinescopFilmPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.feedback_input = "[data-qa-id='movie_review_input']"
        self.accept_feedback_button = "button[data-qa-id='movie_review_submit_button']"
        self.actions_with_review = "button[data-qa-id='movie_review_actions_button']"
        self.written_review_locator = "xpath=/html/body/div[2]/main/div/div/div/div/div[2]/p"


    @allure.step("Написание отзыва и его публикация")
    def write_and_confirm_feedback(self, feedback: str):
        self.enter_text_to_element(self.feedback_input, feedback)
        self.click_element(self.accept_feedback_button)

    @allure.step("Удаление написаного отзыва")
    def delete_feedback(self,):
        self.click_element(self.actions_with_review)
        delete_option = self.page.get_by_role("menuitem", name="Удалить")
        delete_option.click()

    @allure.step("POP UP окно с уведомлением")
    def assert_allert_was_pop_up_feedback(self):
        self.check_pop_up_element_with_text("Отзыв успешно создан")

    def assert_review_was_published_and_equal_written(self, feedback: str):
        review_element = self.page.locator(self.written_review_locator)
        actual_text = review_element.text_content()
        with allure.step("Проверка совдания написанного и опубликованного"):
            assert feedback in  actual_text, "Отзывы не совпадают"
