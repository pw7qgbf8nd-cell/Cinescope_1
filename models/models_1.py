import pytest
from pydantic import BaseModel, Field,  model_validator, field_validator
from venv import logger
from typing import Optional
from enum import Enum
from utils.data_generator import DataGenerator
from constants import Roles

class User(BaseModel):
    email: str
    fullName: str
    password: str = Field(..., min_length=8, max_lenght=40)
    passwordRepeat: str
    verified: Optional[bool] = None
    banned: Optional[bool] = None
    roles: list[Roles]

    # @model_validator(mode="before")
    # def check_email_validation(cls,  values):
    #     if "@" not in values["email"]:
    #         raise ValueError("email должен содержать @")
    #

    @field_validator("email")
    def check_email(cls, value: str) -> str:
        if  "@" not in value:
            raise ValueError("email должен содержать @")
        return value


def get_user(registration_user_data):  # функция get_user возвращает обьект dict с следущими полями
    return registration_user_data

def test_test_user(test_user):
    user_data = User(**get_user(test_user))
    logger.info(f"{user_data.email=} {user_data.fullName=} {user_data.password=} {user_data.banned=} {user_data.verified=} {user_data.roles=}")  # а также возможность удобного взаимодействия
    json_data = user_data.model_dump_json(exclude_unset=True)
    print(json_data)


def test_creation_user_data(creation_user_data):
    user = User(**get_user(creation_user_data))
    logger.info(f"{user.email=} {user.fullName=} {user.password=} {user.banned=} {user.verified=} {user.roles=}")  # а также возможность удобного взаимодействия