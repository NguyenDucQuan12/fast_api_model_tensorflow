from fastapi import APIRouter, Query
from typing import Optional
from pydantic import BaseModel


router = APIRouter(
    prefix="/blog",
    tags=["blog"]
)

class BlogModel(BaseModel):
    title: str
    content : str
    published : Optional[bool]


@router.post("/new/{id}")
def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {
        "id": id,
        "data" : blog,
        "version": version
        }

@router.post("/new/{id}/comment")
def create_comment(blog: BlogModel, id: int, comment: int = Query(None, title= "ID of comment", description= "Some description for comment id")):
    return {
        "id": id,
        "data" : blog,
        "comment_id": comment
        }

def required_functionality():
    return {
        "message":"Learning FastAPI is important"
    }