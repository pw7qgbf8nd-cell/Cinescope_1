import pytest
from API.api_manager import ApiManager
"""Отрефакторить код написанный ранее под использование новых фикстур (например тесты movies)"""
class TestNegMovies:
    def test_get_poster_invalid_data(self, api_manager, super_admin, neg_movies_data):
        super_admin.api.movies_api.get_movies(neg_movies_data,  expected_status=400)

    def test_get_movie_not_found(self, api_manager, super_admin, neg_movie_id ):
        super_admin.api.movies_api.get_movie(neg_movie_id, expected_status=404)
    #     Внесены изменения в строку^

    def test_post_movie_duplicate(self, api_manager,super_admin,  neg_movie_data):
        super_admin.api.movies_api.post_movie(neg_movie_data, expected_status=201)
        super_admin.api.movies_api.post_movie(neg_movie_data, expected_status=409)

    def test_delete_movie_not_found(self, api_manager, neg_movie_id, super_admin):
        super_admin.api.movies_api.delete_movie(neg_movie_id, expected_status=404)

    def test_patch_movie_not_found(self, api_manager,neg_movie_data,super_admin, neg_movie_id, creed_admin):
        super_admin.api.movies_api.patch_movie(neg_movie_data, neg_movie_id, expected_status=404)
# Изменены все тесты

    @pytest.mark.slow
    def test_post_movie_403_common_user(self, api_manager, common_user, movie_data):
        common_user.api.movies_api.post_movie(movie_data, expected_status=403)

#практика 5 модуль, негативный
