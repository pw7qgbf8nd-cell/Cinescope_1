import pytest
from pydantic import BaseModel, Field,  model_validator, field_validator
from venv import logger
from typing import Optional
from enum import Enum
from utils.data_generator import DataGenerator
from constants import Roles



class TypeThing(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHES = "clothes"

class Product(BaseModel):
    name: str = Field(..., min_length=2, max_length=12)
    price: float
    is_stock: bool
    type_thing: TypeThing


laptop = Product(name="MSI", price=12312312.21,  is_stock=True, type_thing=TypeThing.ELECTRONICS)

json_data = laptop.model_dump_json()
print(json_data)

new_data_laptop = Product.model_validate_json(json_data)
print(new_data_laptop)


