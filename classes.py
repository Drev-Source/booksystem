from pydantic import BaseModel


class AgeCategory(BaseModel):
    name: str
    minage: int
    maxage: int


class SkiCategory(BaseModel):
    name: str


class PriceEntry(BaseModel):
    skiid: int
    agecatid: int
    price: int

