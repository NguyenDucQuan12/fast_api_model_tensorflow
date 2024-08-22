from sqlalchemy import create_engine # pip install SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

"""
Định nghĩa cơ sở dữ liệu 
"""

# connection_url = "sqlite:///./fastapi-practice.db" # Dùng để tạo DB sql lite

# Dùng để tạo DB SQL Server
connection_url = URL.create(
    "mssql+pyodbc",
    username="sa",
    password="123456789",
    host="172.31.99.42,1434",
    port=1434,
    database="FastAPI",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "TrustServerCertificate": "yes"
    },
)
engine = create_engine(
    connection_url, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()