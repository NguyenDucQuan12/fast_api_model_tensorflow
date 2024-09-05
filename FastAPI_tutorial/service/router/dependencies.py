from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.param_functions import Depends

router = APIRouter(
    prefix="/dependencies",
    tags=["dependencies"]
)
"""
Các phụ thuộc có thể là các hàm hoặc lớp mà bạn muốn FastAPI thực thi hoặc khởi tạo trước khi thực thi route.  
Dependecies có thể được sử dụng để xử lý xác thực, ủy quyền, kết nối cơ sở dữ liệu, hoặc bất kỳ logic nào khác mà bạn muốn thực hiện trước khi xử lý một yêu cầu.  
Để sử dụng phụ thuộc thì ta cần khai báo `Depends` và truyền hàm hoặc lớp vào `Depends`.  
Có thể áp dụng cho tất cả phụ thuộc vào router bằng cách thêm dependencies = [Depends(function1)] lúc khai báo router = APIRouter  
"""
def convert_headers(request: Request):
    """
    request: Request là một đối tượng đại diện cho yêu cầu HTTP được gửi đến server.  
    Nó bao gồm tất cả thông tin về yêu cầu đó, như phương thức HTTP (GET, POST, v.v.), headers, (body) của yêu cầu, và các tham số truy vấn (query parameters).  
    ## Ví dụ  
    ```python
    name = request.query_params.get('name') or request.form().get('name')
    email = request.query_params.get('email') or request.form().get('email')

    ```
    nếu URL của bạn là /user?name=John&email=john.doe@example.com, thì query_params sẽ chứa {"name": "John", "email": "john.doe@example.com"}.  
    Các tham số có thể tuy vấn từ request: `method: GET, POST, ...`, `url: request.url`, `header`, `query_params: các tham số được truy vấn trong url`
    """
    out_headers = []
    for key, value in request.headers.items():
        out_headers.append(f"{key}--{value}")
    return out_headers

@router.get("")
def get_item(header = Depends(convert_headers)):
    return {
        "items": ["a", "b", "c"],
        "headers": header
    }

@router.post("/new")
def create_item(headers = Depends(convert_headers)):
    return {
        "result": "new item created",
        "headers": headers
    }


class Account():
    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email

@router.post("/user")
def create_user(name:str, email:str, password:str, account: Account = Depends(Account)):
    return{
        "name": account.name,
        "email": account.email 
    }