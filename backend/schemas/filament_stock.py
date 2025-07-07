from pydantic import BaseModel


class FilamentSchema(BaseModel):
    filament_name: str
    color: str
    brand: str
    quantity: float
    activate: bool


class FilamentCreate(FilamentSchema):
    pass


class FilamentOut(FilamentSchema):
    id: int

    class Config:
        orm_mode = True
