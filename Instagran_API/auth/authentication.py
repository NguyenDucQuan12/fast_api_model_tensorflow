from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.models import DbUser
from db.hash import Hash
from auth import oauth2
router = APIRouter(
    tags=["authentication"]
)

# Địa chỉ này phải đúng với tokenURL trong: oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Tạo ra một token có thời gian tồn tại để có thể truy vấn đến các API được khóa  
    - **request** sẽ là dữ liệu theo dạng biểu mẫu của `OAuth2PasswordRequestForm` gồm `username` và `password`  
    Để sử dụng  hàm này ta cần cung cấp `username` và `password` đã được đăng ký trong CSDL  
    ### Ví dụ

    ```python
    import requests

    url_get_token = "http://172.31.99.42:8000/token"
    data = {
        "username": "linh",
        "password": "123456789"
    }
    response = requests.post(url=url_get_token, data= data)
    token = response.json().get("access_token")

    print(token)
    
    ```

    [FastAPI docs for Simple OAuth2 with Password and Bearer](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/)
    """
    user = db.query(DbUser).filter(DbUser.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=f"Not Found User with username: {request.username}"
        )
    hashed_password = user.password
    if not Hash.verify(plain_password= request.password, hashed_password= hashed_password):
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=f"Incorrect Password: {request.username}"
        )
    access_token = oauth2.create_access_token(data= {
        "username": user.username
    })
    return {
        "access_token": access_token,
        "token_type": "bearer", # token tiêu chuẩn: bearer
        "user_id": user.id,
        "username": user.username
    }