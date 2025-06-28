from models.users import User
from sqlalchemy.orm import Session
from schemas.user import UserCreate


def get_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, email=user.email,
                   password=user.password, activate=user.activate)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(user_id: int, user_data: UserCreate, db: Session):
    user = get_user_by_id(db, user_id)
    if user is None:
        return None
    user.username = user_data.username
    user.email = user_data.email
    db.commit()
    db.refresh(user)


def delete_user(user_id: int, db: Session):
    user = get_user_by_id(db, user_id)
    if user is None:
        return None
    db.delete(user)
    db.commit()
    return user
