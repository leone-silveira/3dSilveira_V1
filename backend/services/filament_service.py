from sqlalchemy.orm import Session
from models.filaments import Filament
from schemas.filament_stock import FilamentCreate


def get_filaments(db: Session):
    return db.query(Filament).all()


def get_filament_by_id(db: Session, filament_id: int):
    return db.query(Filament).filter(Filament.id == filament_id).first()

    # filament_name: str
    # color: str
    # brand: str
    # quantity: float
    # activate: bool


def create_filament(db: Session, filament: FilamentCreate):
    db_filament = Filament(filament_name=filament.filament_name,
                           color=filament.color,
                           brand=filament.brand,
                           quantity=filament.quantity,
                           activate=filament.activate)
    db.add(db_filament)
    db.commit()
    db.refresh(db_filament)
    return db_filament


def update_filament(
    filament_id: int,
    filament_data: FilamentCreate,
    db: Session
):
    filament = get_filament_by_id(db, filament_id)
    if filament is None:
        return None

    filament.filament_name = filament_data.filament_name
    filament.color = filament_data.color
    filament.quantity = filament_data.quantity
    filament.brand = filament_data.brand
    filament.activate = filament_data.activate
    db.commit()
    db.refresh(filament)
    return filament


def update_filament_status(filament_id: int, status: bool, db: Session):
    filament = get_filament_by_id(db, filament_id)
    if filament is None:
        return None

    filament.activate = status  # Don't delete just update
    db.commit()
    db.refresh(filament)
    return filament


def delete_filament(filament_id: int, db: Session):
    filament = get_filament_by_id(db, filament_id)
    if filament is None:
        return None

    db.delete(filament)
    db.commit()
    return filament
