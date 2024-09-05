import logging
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from service.schemas import ProductBase
from fastapi import APIRouter, BackgroundTasks
from fastapi.templating import Jinja2Templates

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/templates",
    tags = ["templates"]
)

templates = Jinja2Templates(directory = "service/templates")

@router.get("/products/{id}", response_class= HTMLResponse)
def get_product(id: str, request: Request):
    return templates.TemplateResponse(
        "product.html",
        {
            "request": request,
            "id": id
        }
    )

@router.post("/new_products/{id}", response_class= HTMLResponse)
def get_product(id: str, product: ProductBase, request: Request, bt: BackgroundTasks):

    """
    Truy xuất thông tin về `product` và trả về theo định dạng `HTML`  
    Kèm theo đó là 1 tác vụ nền (background_task) sẽ được thực thi tự động sau khi đã trả kết quả cho người dùng  
    Tác vụ nền này thường được sử dụng để ghi lại nhật ký hoặc gửi email thông báo đển dev nếu một API quan trọng nào đó đã được gọi  
    Cấu trúc tác vụ nền như sau:  
    `bt.add_task(function_send_email, param1, param2, ...)`
    """

    bt.add_task(log_template_call, f"API called with id: {id}")

    return templates.TemplateResponse(
        "new_product_template.html",
        {
            "request": request,
            "id": id,
            "title": product.title,
            "description": product.description,
            "price": product.price
        }
    )

def log_template_call(message: str):
    logger.info(message)