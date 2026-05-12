from API.auth_api import AuthApi
from API.user_api import UserApi
from API.movies_api import MoviesApi

class ApiManager:
    """
       Класс для управления API-классами с единой HTTP-сессией.
       """
    def __init__(self, session):
        """
                Инициализация ApiManager.
                :param session: HTTP-сессия, используемая всеми API-классами.
                """
        self.session = session
        self.auth_api= AuthApi(session)
        self.user_api = UserApi(session)
        self.movies_api = MoviesApi(session)

    def close_session(self):
        self.session.close()
