from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.param_functions import Depends

router = APIRouter(
    prefix="/dependencies",
    tags=["dependencies"]
)

def convert_headers(request: Request):
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