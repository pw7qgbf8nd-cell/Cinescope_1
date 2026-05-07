import pytest
from API.api_manager import ApiManager

class TestNegMovies:
    def test_get_poster_invalid_data(self, api_manager, neg_movies_data):
        api_manager.movies_api.get_movies(neg_movies_data, expected_status=400)

    def test_get_movie_not_found(self, api_manager, neg_movie_id ):
        api_manager.movies_api.get_movie(neg_movie_id, expected_status=404)
    #     Внесены изменения в строку^

    def test_post_movie_duplicate(self, api_manager, creed_admin, neg_movie_data):
        api_manager.auth_api.authenticate(creed_admin)
        api_manager.movies_api.post_movie(neg_movie_data,expected_status=201)
        api_manager.movies_api.post_movie(neg_movie_data, expected_status=409)

    def test_delete_movie_not_found(self, api_manager, neg_movie_id, creed_admin):
        api_manager.auth_api.authenticate(creed_admin)
        api_manager.movies_api.delete_movie(neg_movie_id, expected_status=404)

    def test_patch_movie_not_found(self, api_manager,neg_movie_data, neg_movie_id, creed_admin):
        api_manager.auth_api.authenticate(creed_admin)
        api_manager.movies_api.patch_movie(neg_movie_data, neg_movie_id, expected_status=404)

# Изменены все тесты

