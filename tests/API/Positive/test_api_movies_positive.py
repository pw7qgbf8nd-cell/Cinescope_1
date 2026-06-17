import pytest
from API.api_manager import ApiManager
from utils.data_generator import DataGenerator
import allure
from models.movies_model import MoviesListResponse, MovieResponse

"""Отрефакторить код написанный ранее под использование новых фикстур (например тесты movies)"""
@allure.epic("Проверка позитивной работы API")
@allure.feature("Добавление, удаление, изменение, создание новых фильмов")
@allure.story("CRUD operations")
@allure.severity(allure.severity_level.CRITICAL)
class TestMovies:

    @allure.step("Отправляем GET /movies")
    @pytest.mark.api
    def test_get_movies(self, api_manager, super_admin, movies_data):
        response = super_admin.api.movies_api.get_movies(movies_data)
        response_data = MoviesListResponse(**response.json())
        with allure.step("Шаг 1: Проверка ответа"):
            assert len(response_data.movies) > 0, "Список фильмов пуст"
            assert all(m.genre_id == 3 for m in response_data.movies), "Не все фильмы с жанром 3"




    @allure.step("Отправляем POST /movies")
    @pytest.mark.api
    def test_create_movie(self,api_manager, movie_data, super_admin):
        response = super_admin.api.movies_api.post_movie(movie_data)
        response_data = MovieResponse(**response.json())
        with allure.step("Шаг 1: Проверка ответа"):
            assert response_data.name == movie_data["name"]
            assert response_data.price == movie_data["price"]
            assert response_data.id is not None, "ID должен быть создан"

    @allure.step("Отправляем PATCH /movies")
    @pytest.mark.api
    def test_patch_movie(self, api_manager, created_movie, patch_movie_data, super_admin):
        movie_id = created_movie["id"]
        response = super_admin.api.movies_api.patch_movie(patch_movie_data, movie_id=movie_id)
        response_data = MovieResponse(**response.json())
        with allure.step("Шаг 1: Проверка ответа"):
            assert response_data.name == patch_movie_data["name"]
            assert response_data.id == movie_id

    @allure.step("Отправляем GET by id /movies")
    @pytest.mark.api
    def test_get_movie_id(self, api_manager, created_movie, super_admin):
        movie_id = created_movie["id"]
        response = super_admin.api.movies_api.get_movie(movie_id)
        response_data = MovieResponse(**response.json())
        with allure.step("Шаг 1: Проверка ответа"):
            assert response_data.id == movie_id, "Получили другой фильм"

    @allure.step("Отправляем DELETE /movies")
    @pytest.mark.api
    def test_delete_movie(self, api_manager, created_movie, super_admin):
        movie_id = created_movie["id"]
        super_admin.api.movies_api.delete_movie(movie_id)

    @pytest.mark.api
    @pytest.mark.slow
    @allure.step("Отправляем GET by common user с фильтрацией /movies")
    def test_get_movies_common_user(self, api_manager, common_user, movies_data):
        response = common_user.api.movies_api.get_movies(movies_data)
        response_data = response.json()
        with allure.step("Шаг 1: Проверка ответа"):
            assert set(m["genreId"] for m in response_data["movies"]) == {3}
#Практика из 5 модуля 1 позитивный тест



# Параметризация тест запроса афиши
    @pytest.mark.api
    @allure.step("Отправляем параметризированный POST  /movies")
    @pytest.mark.parametrize("movie_filter",
        [{"genreId": DataGenerator.generate_genre_id()},
        {"locations": DataGenerator.generate_location()},
        {"minPrice": 100, "maxPrice": 1000},
        ], ids=["by_genre", "by_locations", "by_price"])
    def test_get_movies_filtered(self, api_manager, movie_filter):
        response = api_manager.movies_api.get_movies(movie_filter)
        assert response.status_code == 200

# Параметризация тест удаления фильма

    @allure.step("Отправляем параметризированный DELETE  /movies")
    @pytest.mark.slow
    @pytest.mark.parametrize("role_name, expected_status",[("super_admin",200), ("admin_user", 403), ("common_user", 403)],
    ids=["super_admin_delete", "admin_delete", "common_user_delete"])
    def test_delete_movies_parametr_roles(self, api_manager, role_name,expected_status, created_movie, request):
        user = request.getfixturevalue(role_name)
        movie_id = created_movie["id"]
        response = user.api.movies_api.delete_movie(movie_id, expected_status=expected_status)
        assert response.status_code == expected_status

