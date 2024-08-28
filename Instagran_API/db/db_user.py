from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from sqlalchemy import exc
from router.schemas import UserBase
from db.models import DbUser
from db.hash import Hash

def create_user(db: Session, request: UserBase):

    """
    Tạo thông tin người dùng vào CSDL  
    - **username**: Tên người dùng  
    - **email**: Email người dùng  
    - **password**: Mật khẩu người dùng, mật khẩu sẽ được mã hóa `bcrypt`
    """
    
    new_user =  DbUser(
        username = request.username,
        email = request.email ,
        password = Hash.bcrypt(request.password)
    )
    try:
        db.add(new_user)
        db.commit()
        # refresh giúp nhận được giá trị ID của người dùng, vì nó là giá trị tự tăng
        db.refresh(new_user)
    except exc.SQLAlchemyError as e:   
        # Trong quá trình insert lỗi thì giá trị id (cột IDENTITY) vẫn tự tăng, đây là hành vi mặc định của SQL Server
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lỗi khi thêm người dùng mới"
        )
    return new_user 
