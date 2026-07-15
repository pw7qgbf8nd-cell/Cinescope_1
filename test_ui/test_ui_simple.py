from playwright.sync_api import Page, expect
import time
import pytest
from random import randint
from pathlib import Path
from datetime import datetime
import os
from playwright.sync_api import sync_playwright




# def test_text_box(page: Page):
#     page.goto('https://demoqa.com/text-box')
#
#     # вариант №1
#     # username_locator = '#userName'
#     # page.fill(username_locator, 'testQa')
#
#     # вариант №2
#     page.locator('#userName').fill('testQa')
#     page.locator("#userEmail").fill("test@qa.com")
#     page.locator("#currentAddress").fill("москва")
#     page.locator("#permanentAddress").fill("ЗАЖОПИНС")
#     page.click('#submit')  # а можно сразу селектор передать внутрь метода click()
#
#     expect(page.locator('#output #name')).to_have_text('Name:testQa')
#     expect(page.locator('#output #email')).to_have_text('Email:test@qa.com')
#     expect(page.locator('#output #currentAddress')).to_have_text('Current Address :москва')
#     expect(page.locator('#output #permanentAddress')).to_have_text('Permananet Address :ЗАЖОПИНС')
#     # вариант №3
#     # page.fill(selector='#userName', value='testQa')
#
#     time.sleep(10)
'''
def test_text_box_cinescope(page: Page):
    page.goto('https://dev-cinescope.coconutqa.ru/register')
    page.locator('[data-qa-id="register_full_name_input"]').fill('Мелешко Олег Сергеевич')
    page.locator('[data-qa-id="register_email_input"]').fill("test223@email.qa")
    page.locator('[data-qa-id="register_password_input"]').fill("OLEG_AQA25")
    page.locator('[data-qa-id="register_password_repeat_input"]').fill("OLEG_AQA25")
    page.click('[data-qa-id="register_submit_button"]')
    page.wait_for_url('https://dev-cinescope.coconutqa.ru/login')
    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)



    time.sleep(10)
'''

"""
def test_add_comment(page: Page):
    page.goto("https://demoqa.com/webtables")
    page.get_by_role("button", name="add").click()
    modal_title = page.locator('.modal-title:has-text("Registration Form")')
    modal_title.wait_for(state='visible')
    assert modal_title.is_visible(), "Модальное окно не открылось!"
    page.locator('input[placeholder="First Name"]').fill("Мелешко Олег")
    page.locator('input[placeholder="Last Name"]').fill("Сергеевич")
    page.locator('input[placeholder="name@example.com"]').fill("testqa@example.com")
    page.locator('input[placeholder="Age"]').fill("25")
    page.locator('input[placeholder="Salary"]').fill("100000")
    page.locator('input[placeholder="Department"]').fill(" не понял как переводиться")
    page.locator('button#submit').click()
"""


# def test_wright_form(page: Page):
#     page.goto("https://demoqa.com/automation-practice-form")
#     page.get_by_placeholder("First Name").fill("Meleshko")
#     page.get_by_placeholder("Last Name").fill("Oleg")
#     page.get_by_placeholder("name@example.com").fill("testqa@example.com")
#     page.check("#gender-radio-1")
#     page.get_by_placeholder("Mobile Number").fill("9164338152")
#     page.get_attribute("#dateOfBirthInput", "value")
#     page.locator("#subjectsInput").fill("math")
#     page.keyboard.press("Enter")
#     page.check('#hobbies-checkbox-1')
#     page.check("#hobbies-checkbox-2")
#     page.check("#hobbies-checkbox-3")
#     file_path = os.path.abspath("C:/Users/ол/Desktop/я.jpg")
#     page.locator('input[type="file"]').set_input_files(file_path)
#     page.get_by_placeholder("Current Address").fill("МОСКВА")
#     page.locator("#react-select-3-input").click()
#     page.get_by_text("NCR").click()
#     page.locator("#react-select-4-input").click()
#     page.get_by_text("Delhi").click()
#     page.locator('button#submit').click()
#     page.wait_for_selector(".modal-content")
#     assert page.locator(".modal-content").is_visible()



class GooglePage:
    def __init__(self, page):
        self.page = page
        self.url = "https://www.google.com/"

        # Локаторы элементов
        self.search_input = 'textarea[name="q"]'  # Поле ввода запроса
        self.search_button = 'xpath=/html/body/div[2]/div[6]/form/div[1]/div/div[4]/center/input[1]'  # Кнопка "Поиск Google"
        self.lucky_button = 'input[value="Мне повезёт"]'  # Кнопка "Мне повезёт"

    def open(self):
        """Открывает страницу Google."""
        self.page.goto(self.url)

    def enter_search_query(self, query):
        """Вводит текст в строку поиска."""
        self.page.fill(self.search_input, query)

    def click_search_button(self):
        """Нажимает кнопку 'Поиск Google'."""
        self.page.click(self.search_button)

    def click_lucky_button(self):
        """Нажимает кнопку 'Мне повезёт'."""
        self.page.click(self.lucky_button)

    def click_search_button1(self):
        self.page.click(self.search_button)

def test_page_objec():
   with sync_playwright() as playwright:
        # Запуск браузера
        browser = playwright.chromium.launch(headless=False)  # headless=False для визуального отображения
        page = browser.new_page()

        # Создаем объект страницы Google
        google_page = GooglePage(page)

        # Открываем Google
        google_page.open()

        # Вводим запрос и нажимаем кнопку "Поиск Google"
        google_page.enter_search_query("Аниме")
        # time.sleep(2)
        google_page.enter_search_query("Вакансии ?")
        # time.sleep(2)
        google_page.enter_search_query("Page Object что это?")
        # time.sleep(3)
        google_page.click_search_button()
        time.sleep(10)

        # Ждем завершения поиска (например, появления заголовка страницы)
        page.wait_for_selector("h3")  #раскоментируйте если хотите чтоб браузер не закрывался

        # Закрываем браузер
        browser.close()

