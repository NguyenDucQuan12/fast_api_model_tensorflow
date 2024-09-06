from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from sqlalchemy import exc
from router.schemas import CommentBase
from db.models import DbComment
import datetime



def create_comment(db: Session, request: CommentBase, current_user: str):
    """
    Tạo comment cho một bài viết  
    Nội dung comment chứa các thông tin về người viết và nội dung comment
    """
    new_comment = DbComment(
        text = request.text,
        username = current_user,
        post_id = request.post_id,
        timestamp = datetime.datetime.now()
    )

    try:
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
    except exc.SQLAlchemyError as e:   
        # Trong quá trình insert lỗi thì giá trị id (cột IDENTITY) vẫn tự tăng, đây là hành vi mặc định của SQL Server
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lỗi khi tạo comment"
        )
    return new_comment

def get_all_comment(db: Session, post_id: int):
    """
    Truy xuất tất cả comment của một bài viết
    """
    return db.query(DbComment).filter(DbComment.post_id == post_id).all()