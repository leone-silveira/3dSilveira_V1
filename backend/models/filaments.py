from sqlalchemy import Column, Float, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Filament(Base):
    __tablename__ = "filament_stock"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filament_name = Column(String(50), nullable=False)
    color = Column(String(100), nullable=False)
    brand = Column(String(100), nullable=False)
    quantity = Column(Float)
    activate = Column(Boolean, default=True)
