from pydantic import BaseModel
from typing import Union


class BaseSerializer(BaseModel):
    auth: str


class Order(BaseSerializer):
    place: str
    address: str

