from fastapi import APIRouter, Depends, HTTPException
from requests import Session
from database.engine import SessionLocal
from schemas.filament_stock import FilamentCreate, FilamentOut
from services import filament_service

router = APIRouter(tags=["Filament Stock"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[FilamentOut])
def read_filaments(db: Session = Depends(get_db)):
    return filament_service.get_filaments(db)


@router.get("/{filament_id}", response_model=FilamentOut)
def read_filament(
    filament_id: int,
    db: Session = Depends(get_db)
):
    filament = filament_service.get_filament_by_id(db, filament_id)
    if not filament:
        raise HTTPException(status_code=404, detail="filament not found")
    return filament


@router.post("/", response_model=FilamentOut)
def create(
    filament: FilamentCreate,
    db: Session = Depends(get_db)
):
    return filament_service.create_filament(db, filament)


@router.put("/{filament_id}", response_model=FilamentOut)
def update_filament_id(
    filament_id: int,
    filament: FilamentCreate,
    db: Session = Depends(get_db)
):
    try:
        updated = filament_service.update_filament(filament_id, filament, db)
        if updated is None:
            raise HTTPException(
                status_code=404, detail="Filamento não encontrado")
        return updated
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{filament_id}")
def delete_filament_id(
    filament_id: int,
    db: Session = Depends(get_db)
):
    delete_filament_id = filament_service.delete_filament(filament_id, db)
    if delete_filament_id is None:
        raise HTTPException(status_code=404, detail='filament not found')
    return {"detail": "filament deleted successfully"}


@router.put("/{filament_id}/{status}")
def update_filament_status(
    filament_id: int,
    status: bool,
    db: Session = Depends(get_db)
):
    update_filament_status = filament_service.update_filament_status(
        filament_id, status, db)
    if update_filament_status is None:
        raise HTTPException(detail="filament not found")
    return {"detail": f"filament is {status} "}
