import pytest
from API.api_manager import ApiManager

class TestMovies:
    def test_get_movies(self, api_manager, movies_data):
        """Запрос афиши"""
        response = api_manager.movies_api.get_movies(movies_data)
        response_data = response.json()
        assert "movies" in response_data, "Не выводит фильмы"
        assert set(m["genreId"] for m in response_data["movies"]) ==  {3}
    #     Изменен тест + проверка ^
    #Измененил тест(опечатка) Проблема1

    def test_create_movie(self,api_manager, movie_data, creed_admin):
        api_manager.auth_api.authenticate(creed_admin)
        response = api_manager.movies_api.post_movie(movie_data)
        response_data = response.json()
        assert response_data["name"] == movie_data["name"]
        assert response_data["price"] == movie_data["price"]
        #реализация теста через не в сетапе, и можно проверить ответ сервера

    def test_patch_movie(self, api_manager, created_movie, patch_movie_data):
        movie_id = created_movie["id"]
        response = api_manager.movies_api.patch_movie(
            patch_movie_data,
            movie_id=movie_id
        )
        response_data = response.json()
        assert response_data["name"] == patch_movie_data["name"]
        assert response_data["id"] == movie_id

    def test_get_movie_id(self, api_manager, created_movie):
        movie_id = created_movie["id"]
        response = api_manager.movies_api.get_movie(movie_id)
        response_data = response.json()
        assert response_data["id"] == movie_id, "Получили другой фильм"

    def test_delete_movie(self, api_manager, created_movie):
        movie_id = created_movie["id"]
        api_manager.movies_api.delete_movie(movie_id)

