from sqlalchemy import Column, String, Boolean, DateTime, Float
from sqlalchemy.orm import declarative_base
from typing import Dict, Any
import requests
from constants import BASE_URL, Roles
from custom_requester.custom_requester import CustomRequester
from API.api_manager import ApiManager
from models.test_user_models import TestUser
from utils.data_generator import DataGenerator
from resorses.user_creds import SuperAdminCreds
from entities.user import User
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, Boolean, DateTime
from db_requester.db_client import get_db_session
from db_requester.bd_helper import DBHelper
from db_models.moduls.model_user import UserDBModel
from db_models.moduls.model_movies import MovieDBModel

class TestDB:

    def test_create_user_db(self, created_test_user, db_session):
        assert created_test_user.id is not None, "ID пользователя не создан"
        assert created_test_user.email is not None, "Email не создан"
        assert created_test_user.full_name is not None, "Имя не создано"
        user_from_db = db_session.query(UserDBModel).filter(
            UserDBModel.id == created_test_user.id
        ).first()

        assert user_from_db is not None, "Пользователь не найден в БД"
        assert user_from_db.email == created_test_user.email


    def test_create_movie_db(self, created_test_movie, db_session):
        assert created_test_movie.id is not None, "ID фильма не создан"
        assert created_test_movie.name is not None, "имя не создано"
        assert created_test_movie.price is not None, "Цена не создано"
        movie_from_db = db_session.query(MovieDBModel).filter(
            MovieDBModel.id  == created_test_movie.id
        ).first()
        assert movie_from_db is not None, "Фильм не найден в бд"
        assert movie_from_db.price == created_test_movie.price
