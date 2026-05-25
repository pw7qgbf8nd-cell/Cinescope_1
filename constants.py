import utils.data_generator
from enum import Enum

BASE_URL = 'https://auth.dev-cinescope.coconutqa.ru'

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"

MOVIE_ENDPOINT= '/movies'

BASE_URL_MOVIE= "https://api.dev-cinescope.coconutqa.ru"

class Roles(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"

GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'