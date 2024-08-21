from typing import List
from service.db import db_user
from fastapi import APIRouter, Depends
from service.schemas import UserBase, UserDisplay
from service.db.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/user",
    tags=["user"]
)

"""
Tạo các router xử lý với bảng User trong CSDL
"""
@router.post("/", response_model= UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    """
    Tạo phương thức tạo người dùng mới và trả về thông tin theo định dạng UserDisplay
    """
    return db_user.create_user(db, request)

# Read All User
@router.get("/", response_model=List[UserDisplay])
def get_all_user(db: Session = Depends(get_db)):
    """
    Tạo phương thức truy xuất thông tin người dùng và trả về thông tin theo định dạng danh sách UserDisplay
    """
    return db_user.get_all_user(db)

# Read user by id
@router.get("/{id}", response_model= UserDisplay)
def get_user(id: int, db: Session = Depends(get_db)):
    """
    Tạo phương thức truy xuất thông tin một người dùng có id và trả về thông tin theo định dạng UserDisplay
    """
    return db_user.get_user(db=db, id= id)

# Update User
@router.put("/{id}/update")
def update_user(id: int, request: UserBase, db: Session = Depends(get_db)):
    """
    Tạo phương thức cập nhật thông tin một người dùng có id được cung cấp
    """
    return db_user.update_user(db= db, id= id, request= request)

# Delete User
@router.delete("/{id}/delete")
def delete_user(id: int, db: Session = Depends(get_db)):
    """
    Tạo phương thức xóa thông tin một người dùng có id được cung cấp
    """
    return db_user.delete_user(db= db, id= id)