from pydantic import BaseModel


class AgeCategory(BaseModel):
    id: int
    name: str
    minage: int
    maxage: int


class SkiCategory(BaseModel):
    id: int
    name: str


class PriceEntry(BaseModel):
    skiid: int
    agecatid: int
    price: int