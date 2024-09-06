from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.exceptions import HTTPException
import shutil
from sqlalchemy.orm.session import Session
from router.schemas import  PostBase, PostDisplay
from db.database import get_db
from db import db_post
from typing import List
from datetime import datetime
from router.schemas import UserAuth
from auth.oauth2 import get_current_user

"""
Các API liên quan đến các bài viết trong CSDL
"""
router = APIRouter(
    prefix = "/post",
    tags= ["potst"]
)


image_url_type = ["absolute", "relative"]
@router.post("", response_model= PostDisplay)
def create_post(request: PostBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    """
    Tạo thông tin bài đăng vào CSDL  
    Cần xác thực người dùng thì mới có thể tạo bài viết thông qua hàm xác thực `get_current_user`  
    """
    if not request.image_url_type in image_url_type:
        raise HTTPException(status_code= status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail= f"Parameter image type can only take value {image_url_type[0]} or {image_url_type[1]}"
                            )
    
    return db_post.create(db= db, request= request)

@router.get("/all", response_model= List[PostDisplay])
def get_all_post(db: Session = Depends(get_db)):
    """
    Truy xuất tất cả các bài viết trong CSDL
    """
    return db_post.get_all_post(db = db)

@router.post("/image")
def upload_image(image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)):
    """
    Tải hình ảnh lên server và trả về đường dẫn hình ảnh  
    Người dùng có thể dùng kết quả này để làm đường dẫn cho hình ảnh khi tạo bài đăng mới  
    """
    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    now = f"_{current_user.id}_{current_user.username}_{now}." # Định dạng tên file sẽ là "filename_id_username_time.image"
    filename = now.join(image.filename.rsplit(".", 1))
    path = f"files/images/{filename}"

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return {
        "filename": path
    }

@router.delete("/delete/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    """
    Xóa một bài viết  
    Xác thực `user_id` của người xóa và người viết bài có trùng nahu không thì mới cho xóa
    """
    return db_post.delete(db = db, id_post= id, user_id= current_user.id)