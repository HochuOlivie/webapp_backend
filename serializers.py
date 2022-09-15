from pydantic import BaseModel
from typing import Union


class Order(BaseModel):
    place: str
    address: str

