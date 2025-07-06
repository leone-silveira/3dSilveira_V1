from models.users import User
from sqlalchemy.orm import Session
from engine import create_connection


def populate(engine):
    with Session(engine) as session:
        spongebob = User(
            name="spongebob",
            email="spongebob@sqlalchemy.org",
            password='123'
        )
        sandy = User(
            name="sandy",
            addresses="spongebob@sqlalchemy.org",
            password='123'
        )
        session.add_all([spongebob, sandy])
        session.commit()
