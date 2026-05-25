import pytest
from API.api_manager import ApiManager
from conftest import min_max_price, location_msk_spb, genre_id, super_admin, admin_user
from utils.data_generator import DataGenerator

"""Отрефакторить код написанный ранее под использование новых фикстур (например тесты movies)"""
class TestMovies:
    def test_get_movies(self, api_manager,super_admin, movies_data):
        """Запрос афиши"""
        response = super_admin.api.movies_api.get_movies(movies_data)
        response_data = response.json()
        assert "movies" in response_data, "Не выводит фильмы"
        assert set(m["genreId"] for m in response_data["movies"]) ==  {3}
    #     Изменен тест + проверка ^
    #Измененил тест(опечатка) Проблема1

    def test_create_movie(self,api_manager, movie_data, super_admin):
        response = super_admin.api.movies_api.post_movie(movie_data)
        response_data = response.json()
        assert response_data["name"] == movie_data["name"]
        assert response_data["price"] == movie_data["price"]
        #реализация теста через не в сетапе, и можно проверить ответ сервера

    def test_patch_movie(self, api_manager, created_movie, patch_movie_data, super_admin):
        movie_id = created_movie["id"]
        response = super_admin.api.movies_api.patch_movie(patch_movie_data, movie_id=movie_id)
        response_data = response.json()
        assert response_data["name"] == patch_movie_data["name"]
        assert response_data["id"] == movie_id

    def test_get_movie_id(self, api_manager, created_movie, super_admin):
        movie_id = created_movie["id"]
        response = super_admin.api.movies_api.get_movie(movie_id)
        response_data = response.json()
        assert response_data["id"] == movie_id, "Получили другой фильм"

    def test_delete_movie(self, api_manager, created_movie, super_admin):
        movie_id = created_movie["id"]
        super_admin.api.movies_api.delete_movie(movie_id)

    @pytest.mark.slow
    def test_get_movies_common_user(self, api_manager, common_user, movies_data):
        response = common_user.api.movies_api.get_movies(movies_data)
        response_data = response.json()
        assert set(m["genreId"] for m in response_data["movies"]) == {3}
#Практика из 5 модуля 1 позитивный тест



# Параметризация тест запроса афиши
    @pytest.mark.parametrize("movie_filter",
        [{"genreId": DataGenerator.generate_genre_id()},
        {"locations": DataGenerator.generate_location()},
        {"minPrice": 100, "maxPrice": 1000},
        ], ids=["by_genre", "by_locations", "by_price"])
    def test_get_movies_filtered(self, api_manager, movie_filter):
        response = api_manager.movies_api.get_movies(movie_filter)
        assert response.status_code == 200

# Параметризация тест удаления фильма

    @pytest.mark.slow
    @pytest.mark.parametrize("role_name, expected_status",[("super_admin",200), ("admin_user", 403), ("common_user", 403)],
    ids=["super_admin_delete", "admin_delete", "common_user_delete"])
    def test_delete_movies_parametr_roles(self, api_manager, role_name,expected_status, created_movie, request):
        user = request.getfixturevalue(role_name)
        movie_id = created_movie["id"]
        response = user.api.movies_api.delete_movie(movie_id, expected_status=expected_status)
        assert response.status_code == expected_status