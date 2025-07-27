from backend.models.users import User
from backend.models.filaments import Filament
from backend.database.engine import SessionLocal


def populate_db():
    db = SessionLocal()
    try:
        users = [
            User(
                username="leone",
                password="123456",  # ou só "123456" se não tiver hash
                email="leone@example.com",
                activate=True
            ),
            User(
                username="maria",
                password="senha123",
                email="maria@example.com",
                activate=False
            ),
        ]

        filaments = [
            Filament(filament_name="PLA Vermelho", brand="Volt",
                     color="vermelho", quantity=1000, activate=True),
            Filament(filament_name="PLA Preto", brand="Volt",
                     color="preto", quantity=500, activate=True),
        ]
        db.add_all(users + filaments)
        db.commit()
        print("✔ Banco populado com sucesso!")
    except Exception as e:
        db.rollback()
        print("Erro ao popular:", e)
    finally:
        db.close()
