from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from sqlalchemy import exc
from router.schemas import PostBase
from db.models import DbPost
import datetime



def create(db:Session, request: PostBase):
    """
    Tao một bài viết mới lên CSDL  
    Nội dung của một bài viết bao gồm:  
    - **image_url**: Đường dẫn hình ảnh  
    - **image_url_type**: Loại đường dẫn là URL trang web hay đường dẫn hình ảnh có sẵn trong server  
    - **content**: Nội dung của bài viết  
    - **timestamp**: Thời gian đăng tải  
    - **user_id**: ID người đăng bài viết  
    """
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


def get_all_post(db: Session):
    """
    Truy xuất tất cả các bài viết có trong CSDL  

    """
    return db.query(DbPost).all()

def delete(db: Session, id_post: int, user_id: int):
    """
    Xóa một bài viết có `id_post` được cung cấp  
    Khi xóa bài viết thì cần xác thực `user_id` của người xóa và người đăng bài có trùng nhau không  
    """
    post = db.query(DbPost).filter(DbPost.id == id_post).first()

    if not post:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"Post with id {id_post} not found"
        )
    if post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only post creator can delete post"
        )
    db.delete(post)
    db.commit()
    return "Done"