from pydantic import BaseModel
from typing import List

"""
Định nghĩa lược đồ từ người dùng đến API và ngược lại
"""

class Article(BaseModel):
    """
    Class này chứa thông tin về các bài báo sẽ được hiển thị bên trong người dùng khi truy vấn
    Hiển thị trong UesrDisplay
    - **title**: Tên bài báo
    - **content**: nội dung bài báo
    - **published**: đã công bố hay chưa
    """
    title: str
    content: str
    published: bool
    class Config():
        from_attributes  = True

class UserBase(BaseModel):
    """
    Class này chứa thông tin cần được cung cấp từ người dùng 
    - **username**: Tên người dùng
    - **email**: địa chỉ thư điện tử
    - **password**: mật khẩu người dùng
    - **id**: mặc định tự tăng
    """
    username: str
    email: str
    password: str

class UserDisplay(BaseModel):
    """
    Trả về thông tin người dùng theo ý muốn, không trả về những thông tin quan trọng như password đã hash
    Lưu ý tên của các trường thông tin trả về phải giống nhau, nếu không gặp lỗi
    - **username**: tên người dùng
    - **email**: địa chỉ mail của người dùng
    - **items**: Thông tin các bài báo của người này
    -  **Config**: cho phép tự động chuyển đổi dữ liệu type: Database quay trở về kiểu mà ta đã khai báo (str)
    """
    username: str
    email: str
    items: List[Article]= []
    class Config():
        from_attributes  = True

class User(BaseModel):
    """
    Class này chứa thông tin về tác giả sẽ được hiển thị bên trong bài báo khi truy vấn
    Hiển thị trong ArticlesDisplay
    - **id**: id tác giả
    - **username**: tên tác giả
    """
    id: int
    username: str
    class Config():
        from_attributes  = True

class ArticleBase(BaseModel):
    """
    Class này chứa thông tin về các bài báo
    - **username**: Tên người dùng
    - **email**: địa chỉ thư điện tử
    - **password**: mật khẩu người dùng
    - **id**: mặc định tự tăng
    """
    title: str
    content: str
    published: bool
    creator_id: int

class ArticleDisplay(BaseModel):
    title: str
    content: str
    published: bool
    user: User
    class Config():
        from_attributes  = True
