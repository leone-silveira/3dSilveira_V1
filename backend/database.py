from sqlalchemy import create_engine
from sqlalchemy import sessionmaker, declarative_base

DATABASE_URL = (
    "mssql+pyodbc://sa:YourStrong!Passw0rd@localhost:1433/mydatabase?driver=ODBC+Driver+17+for+SQL+Server"
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
