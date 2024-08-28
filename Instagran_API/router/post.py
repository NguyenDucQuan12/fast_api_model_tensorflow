from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from router.schemas import  PostBase, PostDisplay
from db.database import get_db
from db import db_post


router = APIRouter(
    prefix = "/post",
    tags= ["potst"]
)

image_url_type = ["absolute", "relative"]
@router.post("", response_model= PostDisplay)
def create_post(request: PostBase, db: Session = Depends(get_db)):
    """
    Tạo thông tin bài đăng vào CSDL
    """
    if not request.image_url_type in image_url_type:
        raise HTTPException(status_code= status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail= f"Parameter image type can only take value {image_url_type[0]} or {image_url_type[1]}"
                            )
    
    return db_post.create(db= db, request= request)