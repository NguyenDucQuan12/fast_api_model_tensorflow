from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from service.schemas import ProductBase
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
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
def get_product(id: str, product: ProductBase, request: Request):
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