from pydantic import BaseModel


class FilamentSchema(BaseModel):
    name: str
    brand: str
    price: float
    url: str

    class Config:
        from_attributes = True
