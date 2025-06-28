from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Conexão
server = 'localhost'
database = 'master'
username = 'sa'
password = 'YourStrong!Passw0rd'
driver = 'ODBC Driver 17 for SQL Server'

connection_string = f"mssql+pyodbc://{username}:{password}@{server}:1433/{database}?driver={driver.replace(' ', '+')}"
engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base = declarative_base()

# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     username = Column(String(50), nullable=False, unique=True)
#     password = Column(String(100), nullable=False)
#     email = Column(String(100), nullable=False, unique=True)
#     activate = Column(Boolean, default=True)


# Base.metadata.create_all(engine)
