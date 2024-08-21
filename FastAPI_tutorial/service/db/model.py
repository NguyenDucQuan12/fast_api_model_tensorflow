from sqlalchemy.orm import relationship
from service.db.database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.schema import ForeignKey


"""
Định nghĩa Bảng trong CSDL
"""
class DBUser(Base):

    """
    Định nghĩa bảng User trong CSDL
    -**tablename** là tên của bảng 
    - **id** **username**, **email**, **password** là các trường thông tin nằm trong CSDL
    Bảng này sẽ được tạo nếu nó chưa tồn tại trong CSDL
    """
    __tablename__ = "user"
    id = Column(Integer, primary_key= True, index= True)
    username = Column(String(255))
    email = Column(String(255), unique=True) # String(255): kiểu dữ liệu NVARCHAR(255), unique=True chỉ định cột email không được phép trùng lặp
    password = Column(String)
    items = relationship("DBArticles", back_populates = "user")

class DBArticles(Base):

    """
    Định nghĩa bảng Article trong CSDL
    -**tablename** là tên của bảng 
    - **id** **username**, **email**, **password** là các trường thông tin nằm trong CSDL
    Bảng này sẽ được tạo nếu nó chưa tồn tại trong CSDL
    """
    __tablename__ = "article"
    id = Column(Integer, primary_key= True, index= True)
    title = Column(String(255))
    content = Column(String(255), unique=True) # String(255): kiểu dữ liệu NVARCHAR(255), unique=True chỉ định cột email không được phép trùng lặp
    published = Column(Boolean)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("DBUser", back_populates= "items")