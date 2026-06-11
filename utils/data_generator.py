import random
import string
from faker import Faker
from sqlalchemy import Column, String, Boolean, DateTime
import datetime

faker = Faker()

class DataGenerator:
    @staticmethod
    def generate_random_mail():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"ke{random_string}@gmail.com"

    @staticmethod
    def generate_random_int():
        random_int = random.randint(1,10)
        return random_int

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password():
        # Одна буква
        letters = random.choice(string.ascii_letters)
        # Одна цифра
        digits = random.choice(string.digits)

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "&@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6,18)
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_random_invalid_password():
        # Сделаем пароль без цифр
        # Одна буква
        letters = random.choice(string.ascii_letters)

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "&@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(7, 19)
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_random_movie_name():
        random_count = random.randint(1, 112000)
        return f"{random_count} Долматинцев"

    @staticmethod
    def generate_random_price():
        random_price = random.randint(100, 1000)
        return random_price

    @staticmethod
    def generate_genre_id():
        random_id = random.randint(1,9)
        return random_id

    @staticmethod
    def generate_movie_id_neg():
        random_id = random.randint(0, 300000)
        return random_id

    @staticmethod
    def generate_location():
        random_number = random.randint(1,2)
        if random_number == 1:
            return "MSK"
        elif random_number  == 2:
            return "SPB"

    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя"""
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': DataGenerator.generate_random_mail(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }

    @staticmethod
    def generate_movie_data() -> dict:
        """Генерирует данные для тестового фильма"""
        from uuid import uuid4

        return {
            # 'id': f'{uuid4()}',
            'name': DataGenerator.generate_random_movie_name(),
            'price': DataGenerator.generate_random_price(),
            'description': DataGenerator.generate_random_movie_name(),
            'image_url': DataGenerator.generate_random_name(),
            'location': DataGenerator.generate_location(),
            'published': True,
            'rating': DataGenerator.generate_genre_id(),
            'genre_id': DataGenerator.generate_genre_id(),
            'created_at': datetime.datetime.now()
        }
