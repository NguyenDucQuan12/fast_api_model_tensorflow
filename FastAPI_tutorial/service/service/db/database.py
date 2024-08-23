from sqlalchemy import create_engine # pip install SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

"""
Định nghĩa cơ sở dữ liệu 
"""

# connection_url = "sqlite:///./fastapi-practice.db" # Dùng để tạo DB sql lite

# Dùng để tạo DB SQL Server
"""
Kết nối DB SQL Server với SQLAlchemy  
- **username**, **password**: Thông tin đăng nhập  
- **host**: Địa chỉ `IP` máy tính chứa DB, nếu mở cổng khác `1433 (cổng mặc định)` thì sẽ là `IP,PORT`  
- **database**: Tên của CSDL  
- **query**: `phiên bản driver` của SQL Server đang cài trên máy tính và xác thực thông tin
"""
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

#Khi tạo một bảng phải kế thừa `Base`, để Server tự động tạo bảng đó nếu nó chưa tồn tại trong CSDL 
Base = declarative_base()

def get_db():
    """
    Phương thức kết nối tới CSDL  
    Phương thức này sẽ kết nối và sử dụng để truy vấn vào CSDL, sau đó sẽ tự đóng kết nối  
    ## Ví dụ
    ```python
    from sqlalchemy.orm.session import Session
    from fastapi.param_functions import Depends
    from service.db.database import get_db
    from service.db.model import DBUser
    def get_user(id:int, db: Session = Depends(get_db)):
        user = db.query(DBUser).filter(DBUser.id == id).first()
        return user
    ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()