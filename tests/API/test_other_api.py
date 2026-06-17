from sqlalchemy import Column, String, Boolean, DateTime, Float
from sqlalchemy.orm import declarative_base
from typing import Dict, Any
import requests
from constants import BASE_URL, Roles
from custom_requester.custom_requester import CustomRequester
from API.api_manager import ApiManager
from models.test_user_models import TestUser
from utils.data_generator import DataGenerator
from resorses.user_creds import SuperAdminCreds
from entities.user import User
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, Boolean, DateTime
from db_requester.db_client import get_db_session
from db_requester.bd_helper import DBHelper
from db_models.moduls.model_user import UserDBModel
from db_models.moduls.model_movies import MovieDBModel
from db_models.moduls.modul_accounts_transaction_template import AccountTransactionTemplate
import random
import pytest
import allure

@allure.epic("Тестирование транзакций")
@allure.feature("Тестирование транзакций между счетами")
class TestAccountTransactionTemplate:
    @allure.story("Корректность перевода денег между двумя счетами")
    @allure.description("""
        Этот тест проверяет корректность перевода денег между двумя счетами.
        Шаги:
        1. Создание двух счетов: Stan и Bob.
        2. Перевод 200 единиц от Stan к Bob.
        3. Проверка изменения балансов.
        4. Очистка тестовых данных.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Ivan Petrovich")
    @allure.title("Тест перевода денег между счетами 200 рублей")
    def test_accounts_transaction_template(self, db_session: Session):
        # ====================================================================== Подготовка к тесту
        # Создаем новые записи в базе данных (чтоб точно быть уверенными что в базе присутствуют данные для тестирования)
        with allure.step("Создание тестовых данных в базе данных: счета Stan и Bob"):
            stan = AccountTransactionTemplate(user=f"Stan_{DataGenerator.generate_random_int}", balance=1000)
            bob = AccountTransactionTemplate(user=f"Bob_{DataGenerator.generate_random_int}", balance=500)
            db_session.add_all([stan, bob])
            db_session.commit()

        @allure.step("Функция перевода денег: transfer_money")
        @allure.description("""
                    функция выполняющая транзакцию, имитация вызова функции на стороне тестируемого сервиса
                    и вызывая метод transfer_money, мы какбудтобы делем запрос в api_manager.movies_api.transfer_money
                    """)

        def transfer_money(session, from_account, to_account, amount):
            # пример функции выполняющей транзакцию
            # представим что она написана на стороне тестируемого сервиса
            # и вызывая метод transfer_money, мы какбудтобы делем запрос в api_manager.movies_api.transfer_money
            """
            Переводит деньги с одного счета на другой.
            :param session: Сессия SQLAlchemy.
            :param from_account_id: ID счета, с которого списываются деньги.
            :param to_account_id: ID счета, на который зачисляются деньги.
            :param amount: Сумма перевода.
            """
            with allure.step(" Получаем счета"):
                from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
                to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()
            with allure.step("Проверяем, что на счете достаточно средств"):
                if from_account.balance < amount:
                    raise ValueError("Недостаточно средств на счете")

            with allure.step("Выполняем перевод"):
                from_account.balance -= amount
                to_account.balance += amount

            with allure.step("Сохраняем изменения"):
                session.commit()

        # ====================================================================== Тест
        with allure.step("Проверяем начальные балансы"):
            assert stan.balance == 1000
            assert bob.balance == 500

        try:
            with allure.step("Выполняем перевод 200 единиц от stan к bob"):
                transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=200)


            with allure.step("Проверяем, что балансы изменились"):
                assert stan.balance == 800
                assert bob.balance == 700

        except Exception as e:

            with allure.step("ОШИБКА откаты транзакции"):
                db_session.rollback()  # откат всех введеных нами изменений
                pytest.fail(f"Ошибка при переводе денег: {e}")

        finally:
            with allure.step("Удаляем данные для тестирования из базы"):
                db_session.delete(stan)
                db_session.delete(bob)
                db_session.commit()
