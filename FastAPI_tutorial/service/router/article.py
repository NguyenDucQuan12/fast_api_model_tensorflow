from typing import List
from service.db import db_article
from fastapi import APIRouter, Depends
from service.schemas import ArticleBase, ArticleDisplay
from service.db.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/article",
    tags=["article"]
)

"""
Tạo các router xử lý với bảng Article trong CSDL
"""

# create Article
@router.post("/", response_model= ArticleDisplay)
def create_article(request: ArticleBase, db: Session = Depends(get_db)):
    return db_article.create_article(db= db, request= request)

# Get specific article
@router.get("/{id}", response_model= ArticleDisplay)
def get_article(id: int, db: Session = Depends(get_db)):
    return db_article.get_article(db= db, id= id)