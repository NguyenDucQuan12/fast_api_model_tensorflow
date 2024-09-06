from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from router.schemas import  CommentBase
from db.database import get_db
from db import db_comment
from router.schemas import UserAuth
from auth.oauth2 import get_current_user

"""
Các API về comment
"""
router = APIRouter(
    prefix = "/comment",
    tags= ["comment"]
)

@router.get("/all/{post_id}")
def comments(post_id: int, db: Session = Depends(get_db)):
    """
    Truy xuất tất cả comment của một bài đăng có `post_id`  
    """
    return db_comment.get_all_comment(db= db, post_id= post_id)

@router.post("")
def create(request: CommentBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    """
    Tạo một comment cho bài viết  
    Cần xác thực người dùng xong mới có thể tạo comment  
    """
    return db_comment.create_comment(db= db, request= request, current_user= current_user.username)