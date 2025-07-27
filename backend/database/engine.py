from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Conexão
server = 'mssql'
database = 'master'
username = 'sa'
password = 'YourStrong!Passw0rd'
driver = 'ODBC Driver 17 for SQL Server'

connection_string = (
    f"mssql+pyodbc://{username}:{password}@{server}:1433/{database}"
    f"?driver={driver.replace(' ', '+')}&TrustServerCertificate=yes"
)
engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
