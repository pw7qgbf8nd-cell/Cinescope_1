import pytest
"""### **2. Реализовать негативные проверки**

**Описание:** нужно написать тесты на негативные сценарии для авторизации.

**Пример заданий:**

1. Попробуйте авторизоваться с неверным паролем:
    - Ожидается статус код `401` или `500` (в зависимости от версии приложения)
    - Тело ответа должно содержать сообщение об ошибке
2. Попробуйте авторизоваться с несуществующим email:
    - Ожидается статус код `401`
    - Тело ответа должно содержать сообщение об ошибке
3. Попробуйте авторизоваться с пустым телом запроса"""

class TestNegApi:
    def test_auth_neg_password(self,api_manager, test_user_neg):
        api_manager.auth_api.login_user(test_user_neg, expected_status=401)
    #     Изменен тест^


    def test_auth_neg_email(self,api_manager, test_user_neg):
        api_manager.auth_api.login_user(test_user_neg, expected_status=401)


    def test_auth_neg_body(self, api_manager, invalid_body):
        api_manager.auth_api.login_user(invalid_body, expected_status=401)
#     Изменены тесты^