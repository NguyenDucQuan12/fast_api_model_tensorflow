from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from sqlalchemy import exc
from router.schemas import PostBase
from db.models import DbPost
import datetime



def create(db:Session, request: PostBase):
    new_post = DbPost(
        image_url = request.image_url,
        image_url_type = request.image_url_type,
        content = request.content,
        timestamp = datetime.datetime.now(),
        user_id = request.creator_id
    )
    try:
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
    except exc.SQLAlchemyError as e:   
        # Trong quá trình insert lỗi thì giá trị id (cột IDENTITY) vẫn tự tăng, đây là hành vi mặc định của SQL Server
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lỗi khi tạo bài đăng mới"
        )
    return new_post