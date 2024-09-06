from pydantic import BaseModel
from datetime import datetime
from typing import List

"""
Khai báo các định nghĩa kiểu trả về  
Lưu ý:  
- ` Tên các trường phải trùng khớp với các trường đã khai báo khi tạo bảng`  
## Ví dụ:  
```python
# Định dạng kiểu trả về phải có tên trùng với bảng đã tạo  
class PostDisplay(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    content: str
    timestamp: datetime
    user: user_in_post
    comments: List[comment_in_post]
    class Config():
        from_attributes  = True

# Bảng tạo trong cơ sở dữ liệu có các trường `id`, ..., `comments`  
class DbPost(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key= True, index= True)
    image_url = Column(String)
    image_url_type = Column(String)
    content = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("DbUser", back_populates= "items")
    comments = relationship("DbComment", back_populates= "post")
```
"""

class UserBase(BaseModel):
    username: str
    email:str
    password: str

class UserDisplay(BaseModel):
    username: str
    email:str
    class Config():
        from_attributes  = True

class user_in_post(BaseModel):
    username: str
    class Config():
        from_attributes  = True

class comment_in_post(BaseModel):
    text: str
    username: str
    timestamp: datetime
    class Config():
        from_attributes  = True

class PostBase(BaseModel):
    image_url: str
    image_url_type: str
    content: str
    creator_id: int

class PostDisplay(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    content: str
    timestamp: datetime
    user: user_in_post
    comments: List[comment_in_post]
    class Config():
        from_attributes  = True

class UserAuth(BaseModel):
    id: int
    username: str
    email: str

class CommentBase(BaseModel):
    text: str
    post_id: int