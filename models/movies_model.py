from sqlalchemy import Column, String, Boolean, DateTime, Float, INTEGER
from sqlalchemy.orm import declarative_base
from typing import Dict, Any, List
from pydantic import BaseModel, Field,  model_validator, field_validator, ConfigDict
from constants import Roles
from typing import Optional


Base = declarative_base()

class GenreInfo(BaseModel):
    name: Optional[str] = None


class MovieResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    name: str
    price: int
    description: str
    image_url: Optional[str] = Field(None, alias="imageUrl")
    location: str
    published: bool
    rating: int
    genre_id: int = Field(alias="genreId")
    genre: Optional[GenreInfo]  = None
    created_at: str = Field(alias="createdAt")


class MoviesListResponse(BaseModel):
    """Модель ответа на GET /movies — список фильмов"""
    movies: List[MovieResponse]
    page: int
    pageSize: int = Field(alias="pageSize")
    count: int
    pageCount: int = Field(alias="pageCount")