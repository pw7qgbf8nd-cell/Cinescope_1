from constants import MOVIE_ENDPOINT, BASE_URL_MOVIE
from custom_requester.custom_requester import CustomRequester


class MoviesApi(CustomRequester):
    """CLASS для работы с запросами по фильмам"""
    
    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL_MOVIE)

    def get_movies(self, poster_data, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=MOVIE_ENDPOINT,
            params=poster_data,
            expected_status=expected_status
        )
    # Правка была выше^ (передача querry параметров не в data  а в param)

    def post_movie(self, movie_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint=MOVIE_ENDPOINT,
            data=movie_data,
            expected_status=expected_status
        )

    def get_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def patch_movie(self, patch_movie_data, movie_id, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            data=patch_movie_data,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )
    # удалены все негативные методы^