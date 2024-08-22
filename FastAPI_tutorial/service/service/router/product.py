from fastapi import APIRouter, Header, Cookie
from typing import Optional, List
from fastapi.responses import Response
from fastapi.responses import HTMLResponse
from fastapi.responses import PlainTextResponse
import time


router = APIRouter(
    prefix="/product",
    tags=["product"]
)

products = ["watch", "camera", "phone"]

async def time_consuming_functionality():
    """
    Mô phỏng một chức năng tiêu tốn thời gian bằng cách tạm dừng 5 giây   
    Để 1 hàm có thể sử dụng được 2 chức năng này thì phải đánh dấu nó là **async** trước lúc khởi tạo hàm  
    ví dụ: **async def time_consuming_functionality()**  
    """
    time.sleep(5)
    return "Done 5s"

@router.get("/")
async def get_all_product():
    """
    Lấy tất cả giá trị trong products và lưu cookie  
    Việc có thêm hàm **time_consuming_functionality** sẽ làm cho API này phải đợi 5s trước khi thực hiện các chức năng bên dưới nó  
    Khi đánh dấu là **await** (hàm được đánh dấu phải được khai báo là **async**) thì khi gọi đến API get_all_product 
    sẽ tạm dừng tại hàm **await** cho đến khi hàm này chạy xong thì các câu lệnh bên dưới nó mới tiếp tục   
    Tuy nhiên nó sẽ không chặn toàn bộ chương trình, trong lúc đang đợi cho hàm **await** hoàn thành thì vẫn có thể thực hiện các API khác, hoặc nhận các lệnh API gọi đến 
    hàm get_all_product thêm lần nữa
    """
    await time_consuming_functionality()
    data = " ".join(products) # chuyển đổi thành dạng văn bản  và phản hổi với người dùng bằng Response
    response = Response(content= data, media_type= "text/plain")
    response.set_cookie(key= "test_cookie", value= "cookie_value")
    return response

@router.get("/cookie")
def get_cookie(test_cookie : Optional[str] = Cookie(None)):
    """
    Lấy cookie  
    Lưu ý tên biến phải trùng với **key** cookie đã lưu  
    ví dụ **key = "test_cookie"** thì tên biến cũng phải là **test_cookie**
    """
    cookie = test_cookie
    return {
        "cookie": cookie
    }

@router.get("/withheader")
def get_product_with_header(
    response: Response,
    custom_header: Optional[List[str]] = Header(None) # custom_header: Optional[str] = Header(None)
):
    """
    Lấy giá trị với header  
    Để kiểm tra header thì vào trang web nhấn **F12** hoặc **Inspect** và vào mục **Network**  
    Sau đó chạy thử API để xem giá trị network nhận về
    """
    # Nếu muốn trả về header thì thêm câu lệnh bên dưới, nếu ko thì ko cần câu lệnh dưới
    response.headers["custom_my_header"] = "and".join(custom_header)
    return products


"""
Chỉnh sửa lại tài liệu các mã trạng thái trả về của router theo cấu trúc như sau:  
mã code: {  
    "content" :{  
        "kiểu trả về": {  
        "example": "viết mô tả về ví dụ"  
        }  
    },  
    "description": "Viết mô tả về mã code này"  
}  
"""
@router.get("/{id}", responses= {
    200: {
        "content":{
            "text/html": {
                "example": "<div> Product</div>"
            }
        },
        "description": "Return the HTML for an object"
    },
    404: {
        "content":{
            "text/plain": {
                "example": "Product not available"
            }
        },
        "description": "A cleartext error message"
    },
})
def get_product(id: int):
    """
    Trả về định dạng văn bản thuần túy với **PlainTextResponse** của fastapi  
    Trả về định dạng HTML với thư viện **HTMLResponse** của fastapi   
    Để kiểm tra HTML thì vào đường link sau và dán câu lệnh HTML: https://htmlg.com/html-editor/  
    Lưu ý bỏ bớt 1 ngoặc nhọn ở **.product** khi kiểm tra, còn viết thì vẫn để 2 ngoặc nhọn
    """
    if id> len(products):
        out = "Product not available"
        return PlainTextResponse(content= out, media_type= "text/plain", status_code= 400)
    else:
        product = products[id]
        out = f"""
        <head>
            <style>
            .product {{
                width: 500px;
                height: 30px;
                border: 2px inset green;
                background-color: lightblue;
                text-align: center;

            }}
            </style>
        </head>
        <div class="product">{product}</div>
        """
        return HTMLResponse(content= out, media_type="text/html")