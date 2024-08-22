from service.db.model import DBArticles
from sqlalchemy.orm.session import Session
from service.schemas import ArticleBase
from fastapi import HTTPException, status
from sqlalchemy import exc


def create_article(db: Session, request: ArticleBase):
    new_article = DBArticles(
        title = request.title,
        content = request.content,
        published = request.published,
        user_id =request.creator_id
    )
    try:
        db.add(new_article)
        db.commit()
        # refresh giúp nhận được giá trị ID của người dùng, vì nó là giá trị tự tăng
        db.refresh(new_article)
    except exc.SQLAlchemyError as e:   
        # Trong quá trình insert lỗi thì giá trị id (cột IDENTITY) vẫn tự tăng, đây là hành vi mặc định của SQL Server
        db.rollback()
        # Ném ra HTTPException với mã trạng thái 400 và thông báo lỗi
        # Nếu không thì dù insert lỗi nhưng mã trạng thái vẫn là 200
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lỗi khi thêm bài báo mới"
        )
    return new_article

def get_article(db: Session, id: int):
    article = db.query(DBArticles).filter(DBArticles.id == id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy bài báo"
        )
    return article