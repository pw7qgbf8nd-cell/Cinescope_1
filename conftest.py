
from faker import Faker
import pytest
import requests
from constants import BASE_URL, Roles
from custom_requester.custom_requester import CustomRequester
from API.api_manager import ApiManager
from models.base_models import TestUser
from utils.data_generator import DataGenerator
from resorses.user_creds import SuperAdminCreds
from entities.user import User
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, Boolean, DateTime
from db_requester.db_client import get_db_session
from db_requester.bd_helper import DBHelper

faker = Faker()

@pytest.fixture
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_mail(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )

@pytest.fixture(scope="session")
def auth_admin(api_manager, creed_admin):
    api_manager.auth_api.authenticate(creed_admin)
    yield api_manager.movies_api.session.headers.get("Authorization")
# создана фикстура^

@pytest.fixture
def test_user_neg():
    return {
        "email": DataGenerator.generate_random_mail(),
        "password": DataGenerator.generate_random_password()
    }
# Были изменения,  создана факстура ^

@pytest.fixture(scope="session")
def creed_admin():
    return ["api1@gmail.com", "asdqwe123Q"]

@pytest.fixture(scope="session")
def movies_data():
    return {
      "genreId": 3
    }
# Измененена фикстура ^

@pytest.fixture(scope="function")
def movie_data():
    return {
        "name": DataGenerator.generate_random_movie_name(),
        "imageUrl": "https://image.url",
        "price": DataGenerator.generate_random_price(),
        "description": "ТЕСТТЕСТЕСТЕТСТЕСТЕСТ",
        "location": "SPB",
        "published": True,
        "genreId": DataGenerator.generate_genre_id()
    }
# Поправлена фикстура^
# изменена фикстура, скоуп финкция

@pytest.fixture
def neg_movie_id():
    return DataGenerator.generate_movie_id_neg()

@pytest.fixture(scope="session")
def patch_movie_data():
    random_price = DataGenerator.generate_random_price()
    random_name = DataGenerator.generate_random_movie_name()
    return {
  "name": random_name,
  "description": "Movie description",
  "price": random_price,
  "location": "SPB",
  "imageUrl": "https://image.url",
  "published": True,
  "genreId": 1
}

@pytest.fixture
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(user_data=test_user.model_dump())
    response_data = response.json()
    registered_user = test_user.model_copy(update={"id": response_data["id"]})
    return registered_user
# изменена фикстура

@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope="session")
def session():
    """
        Фикстура для создания HTTP-сессии.
        """
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    """
       Фикстура для создания экземпляра ApiManager.
       """
    return ApiManager(session)

@pytest.fixture
def created_movie(api_manager, auth_admin, movie_data):
    # 1. Создаём фильм (POST)
    response = api_manager.movies_api.post_movie(movie_data)
    created = response.json()
    movie_id = created["id"]

    # 2. Возвращаем данные теста́м
    yield {**movie_data, "id": movie_id}
    try:
        api_manager.movies_api.delete_movie(movie_id, expected_status=200)
    except ValueError:
        pass
#     Поправлена фикстура ^

@pytest.fixture(scope="session")
def neg_movie_data():
    return {
        "name": DataGenerator.generate_random_name(),
        "imageUrl": "https://image.url",
        "price": 100,
        "description": "ТЕСТТЕСТЕСТЕТСТЕСТЕСТ",
        "location": "SPB",
        "published": True,
        "genreId": 1
    }

@pytest.fixture(scope="session")
def neg_movies_data():
    return {
        "page": -1,
        "pageSize": 999999,
        "genreId": "invalid"
    }

@pytest.fixture
def invalid_body():
    return {}

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope="function")
def creation_user_data(test_user) -> TestUser:
    return test_user.model_copy(update={
        "verified": True,
        "banned": False
    })

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def admin_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.ADMIN.value],
        new_session
    )
    super_admin.api.user_api.create_user(creation_user_data)
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user

@pytest.fixture
def min_max_price():
    return DataGenerator.generate_random_price()

@pytest.fixture
def location_msk_spb():
    return DataGenerator.generate_location()

@pytest.fixture
def genre_id():
    return DataGenerator.generate_genre_id()
@pytest.fixture(params=[
    {"genreId": genre_id},
    {"locations": location_msk_spb},
    {"minPrice": 100, "maxPrice": 1000}])
def movie_filter(request):
    return request.param

@pytest.fixture
def registration_user_data():
    random_password = DataGenerator.generate_random_password()

    return {
        "email": DataGenerator.generate_random_mail(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }

@pytest.fixture(scope="module")
def db_session() -> Session:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)

@pytest.fixture(scope="function")
def created_test_movie(db_helper):
    movie = db_helper.create_test_movie(DataGenerator.generate_movie_data())
    yield movie
    if db_helper.get_movie_by_name(movie.name):
        db_helper.delete_movie(movie)