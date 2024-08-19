from fastapi import APIRouter
from service.router.blog_post import required_functionality
from typing import Optional
from fastapi import Response, status, Depends

# xác định router với tiền tố là /blog, khi một router.get.post.put được tạo thì mặc định /blog sẽ được thêm vào trước đường dẫn
# Các hàm được tạo sẽ được tự động thêm tag vào
router = APIRouter(
    prefix="/blog",
    tags= ["blog"]
)

# truyền hàm required_functionality vào biến req_parameter
@router.get("/home/{id}/comments/{comments_id}")
def get_comment(id: int, comments_id: int, req_parameter: dict = Depends(required_functionality), user_name : Optional[str] = None):

    """
    Hàm này lấy giá trị id cùng với comment của một người
    - **id** là tham số bắt buộc
    - **comments_id** là tham số bắt buộc
    - **valid** là tham số bắt buộc
    - **user_name** là tham số tùy chọn
    """
    return {"Message": f"You are here comments_id: {comments_id} and user_name: {user_name}",
            "request": req_parameter
            }

@router.get("/{id}", status_code= status.HTTP_200_OK)
def get_blog(id: int, response: Response):
    if id>7:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"{id} not accept"}
    else:
        response.status_code = status.HTTP_200_OK
        return {"Message ": f"xin chào id {id}"}


