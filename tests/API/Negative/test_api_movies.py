import pytest
from API.api_manager import ApiManager
import allure

"""Отрефакторить код написанный ранее под использование новых фикстур (например тесты movies)"""
@allure.epic("Проверка негативной работы API")
@allure.feature("Добавление, удаление, изменение, создание новых фильмов")
@allure.story("CRUD operations")
@allure.severity(allure.severity_level.CRITICAL)
class TestNegMovies:

    @allure.step("Отправляем invalid GET (с несущуствующими данными)/movies")
    @pytest.mark.api
    def test_get_poster_invalid_data(self, api_manager, super_admin, neg_movies_data):
        with allure.step("Шаг 1: Проверка ответа"):
            super_admin.api.movies_api.get_movies(neg_movies_data,  expected_status=400)

    @allure.step("Отправляем invalid GET (поиск по не существующему id)/movies")
    @pytest.mark.api
    def test_get_movie_not_found(self, api_manager, super_admin, neg_movie_id ):
        with allure.step("Шаг 1: Проверка ответа"):
            super_admin.api.movies_api.get_movie(neg_movie_id, expected_status=404)

    @allure.step("Отправляем invalid POST (попытка создания уже существующего фильма)/movies")
    @pytest.mark.api
    def test_post_movie_duplicate(self, api_manager,super_admin,  neg_movie_data):
        super_admin.api.movies_api.post_movie(neg_movie_data, expected_status=201)
        with allure.step("Шаг 1: Проверка ответа"):
            super_admin.api.movies_api.post_movie(neg_movie_data, expected_status=409)

    @allure.step("Отправляем invalid DELETE (попытка удаления несуществующего фильма)/movies")
    @pytest.mark.api
    def test_delete_movie_not_found(self, api_manager, neg_movie_id, super_admin):
        with allure.step("Шаг 1: Проверка ответа"):
            super_admin.api.movies_api.delete_movie(neg_movie_id, expected_status=404)

    @allure.step("Отправляем invalid PATCH (попытка изменения несуществующего фильма)/movies")
    @pytest.mark.api
    def test_patch_movie_not_found(self, api_manager,neg_movie_data,super_admin, neg_movie_id, creed_admin):
        with allure.step("Шаг 1: Проверка ответа"):
                super_admin.api.movies_api.patch_movie(neg_movie_data, neg_movie_id, expected_status=400)
# Изменены все тесты
    @allure.step("Отправляем POST (попытка создания фильма при отсутствии прав на создание)/movies")
    @pytest.mark.slow
    def test_post_movie_403_common_user(self, api_manager, common_user, movie_data):
        with allure.step("Шаг 1: Проверка ответа"):
            common_user.api.movies_api.post_movie(movie_data, expected_status=403)

#практика 5 модуль, негативный
