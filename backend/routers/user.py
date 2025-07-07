from fastapi import APIRouter, Depends, HTTPException
from database.engine import SessionLocal
from sqlalchemy.orm import Session
from services import user_service
from schemas.user import UserCreate, UserOut

router = APIRouter(tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[UserOut])
def read_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)


@router.get("/{user_id}", response_model=UserOut)
def read_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserOut)
def create(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return user_service.create_user(db, user)


@router.put("/{user_id}", response_model=UserOut)
def update_user_id(
    user_id: int,
    user: UserCreate,
    db: Session = Depends(get_db)
):
    update_user_id = user_service.update_user(user_id, user, db)
    if update_user_id is None:
        raise HTTPException(status_code=404, detail='User not found')
    return update_user_id


@router.delete("/{user_id}")
def delete_user_id(
    user_id: int,
    db: Session = Depends(get_db)
):
    delete_user_id = user_service.delete_user(user_id, db)
    if delete_user_id is None:
        raise HTTPException(status_code=404, detail='User not found')
    return {"detail": "User deleted successfully"}


@router.put("/{user_id}/{status}")
def update_user_status(
    user_id: int,
    status: bool,
    db: Session = Depends(get_db)
):
    update_user_status = user_service.update_user_status(user_id, status, db)
    if update_user_status is None:
        raise HTTPException(detail="User not found")
    return {"detail": f"User is {status} "}
