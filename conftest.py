
from faker import Faker
import pytest
import requests
from constants import BASE_URL, Roles
from custom_requester.custom_requester import CustomRequester
from API.api_manager import ApiManager
from utils.data_generator import DataGenerator
from resorses.user_creds import SuperAdminCreds
from entities.user import User

faker = Faker()

@pytest.fixture
def test_user():
    random_password = DataGenerator.generate_random_password()
    return {
        "email": DataGenerator.generate_random_mail(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

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
    response = api_manager.auth_api.register_user(test_user)
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
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
def creation_user_data(test_user):
    updated_data = test_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data["email"],
        creation_user_data["password"],
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

