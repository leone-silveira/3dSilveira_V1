from pydantic import BaseModel


class FilamentPriceSchema(BaseModel):
    name: str
    brand: str
    price: float
    url: str

    class Config:
        from_attributes = True
