from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from service import schemas
from service.db.model import DBUser
from service.db.hash import Hash
from sqlalchemy import exc


"""
Các hàm thực hiện chức năng với Database
- **create_user** là tạo thông tin người dùng và lưu vào DB
- **get_all_user** truy xuất thông tin của bảng user
- **get_user** truy xuất thông tin người dùng trong CSDL theo id
- **update_user** cập nhật thông tin người dùng trong CSDL theo id
- **delete_user** xóa thông tin người dùng khỏi CSDL theo id
"""

def create_user(db: Session, request: schemas.UserBase):

    """
    Thêm người dùng mới vào DB
    Chuyển đổi loại dữ liệu từ người dùng (UserBase) sang dữ liệu lưu vào CSDL (DBUser)

    - **new_user**: là trường thông tin của người dùng mới, bao gồm tên, email, mật khẩu
    - **mật khẩu**: sẽ được mã hóa trước khi đưa vào DB

    Xử lý ngoại lệ nếu quá trình thêm vào CSDL bị lỗi thì sẽ rollback lại và đưa ra trạng thái lỗi 400
    """
    new_user = DBUser(
        username = request.username,
        email = request.email,
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
        # Ném ra HTTPException với mã trạng thái 400 và thông báo lỗi
        # Nếu không thì dù insert lỗi nhưng mã trạng thái vẫn là 200
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lỗi khi thêm người dùng mới"
        )
    return new_user

def get_all_user(db: Session):
    """
    Lấy ra thông tin của tất cả người dùng
    - **username**: tên người dùng
    - **email**: thư điện tử
    """
    return db.query(DBUser).all()

def get_user(db: Session, id: int):
    """
    Lấy ra thông tin của người dùng theo id được cung cấp
    - **id**: id của người dùng
    Trả về thông tin người dùng
    - **username**: tên người dùng
    - **email**: thư điện tử
    Xử lý ngoại lệ nếu không tìm thấy người dùng có id đã cung cấp
    """
    user = db.query(DBUser).filter(DBUser.id == id).first()
    # user = db.query(DBUser).filter(DBUser.id == id).filter(DBUser.email == email).first()

    if not user:
        # Ném ra HTTPException nếu không tìm thấy người dùng với id tương ứng
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Người dùng không tồn tại"
        )
    
    return user
def get_user_by_username(db: Session, username: str):
    """
    Lấy ra thông tin của người dùng theo id được cung cấp
    - **id**: id của người dùng
    Trả về thông tin người dùng
    - **username**: tên người dùng
    - **email**: thư điện tử
    Xử lý ngoại lệ nếu không tìm thấy người dùng có id đã cung cấp
    """
    user = db.query(DBUser).filter(DBUser.username == username).first()
    # user = db.query(DBUser).filter(DBUser.id == id).filter(DBUser.email == email).first()

    if not user:
        # Ném ra HTTPException nếu không tìm thấy người dùng với id tương ứng
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Người dùng không tồn tại"
        )
    
    return user

def update_user(db: Session, id: int, request: schemas.UserBase):
    """
    Cập nhật thông tin của người dùng có id được cung cấp
    - **username**: tên người dùng
    - **email**: thư điện tử
    - **password**: mật khẩu người dùng

    Xử lý ngoại lệ nếu không tìm thấy người dùng có id đã cung cấp
    Xử lý ngoại lệ nếu quá trình cập nhật thông tin lỗi thì rollback
    """
    user = db.query(DBUser).filter(DBUser.id == id).first()

    if not user:
        # Ném ra HTTPException nếu không tìm thấy người dùng với id tương ứng
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Người dùng không tồn tại"
        )
    
    # Cập nhật các thuộc tính của đối tượng user
    user.username = request.username
    user.email = request.email
    user.password = Hash.bcrypt(request.password)

    try:
        db.commit()
    except exc.SQLAlchemyError as e:   
        db.rollback()
        # Ném ra HTTPException với mã trạng thái 400 và thông báo lỗi
        # Nếu không thì dù update lỗi nhưng mã trạng thái vẫn là 200
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lỗi khi cập nhật người dùng"
        )
    return "done"

def delete_user(db: Session, id: int):
    """
    Xóa thông tin của người dùng có id được cung cấp
    Xử lý ngoại lệ nếu không tìm thấy người dùng có id đã cung cấp
    Xử lý ngoại lệ nếu quá trình cập nhật thông tin lỗi thì rollback
    """
    user = db.query(DBUser).filter(DBUser.id == id).first()

    if not user:
        # Ném ra HTTPException nếu không tìm thấy người dùng với id tương ứng
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Người dùng không tồn tại"
        )
    
    db.delete(user)

    try:
        db.commit()
    except exc.SQLAlchemyError as e:   
        db.rollback()
        # Ném ra HTTPException với mã trạng thái 400 và thông báo lỗi
        # Nếu không thì dù update lỗi nhưng mã trạng thái vẫn là 200
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lỗi khi xóa người dùng"
        )
    return "done"