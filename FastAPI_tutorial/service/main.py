# import tensorflow as tf

from fastapi import FastAPI
from service.api.api import main_router
from service.router import blog_get, blog_post
from service.db import model
from service.db.database import engine

app = FastAPI(project_name = "TestAPI")

app.include_router(blog_get.router)
app.include_router(blog_post.router)
# app.include_router(main_router)

# Tải mô hình 1 lần khi chạy server, các lần dự đoán sẽ không phải tải mô hình nữa
# load_save_model = tf.keras.models.load_model(".FastAPI/service/core/logic/Malaria_model_save.keras")
load_save_model = None

@app.get("/")
def read_root():
    return {"Message": "World"}

model.Base.metadata.create_all(engine)
