from pydantic import BaseModel
from datetime import datetime

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
    class Config():
        from_attributes  = True