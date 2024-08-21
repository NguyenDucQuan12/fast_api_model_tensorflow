# import tensorflow as tf
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from service.router import blog_get, blog_post, user
from service.router import article
from service.router import product
from service.router import file
from service.auth import authentication
from service.db import model
from service.db.database import engine

app = FastAPI(project_name = "TestAPI")

app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(blog_post.router)
app.include_router(product.router)
app.include_router(article.router)
app.include_router(authentication.router)
app.include_router(file.router)
# app.include_router(main_router)

# Tải mô hình 1 lần khi chạy server, các lần dự đoán sẽ không phải tải mô hình nữa
# load_save_model = tf.keras.models.load_model(".FastAPI/service/core/logic/Malaria_model_save.keras")
load_save_model = None

@app.get("/")
def read_root():
    return {"Message": "World"}

# Tạo Bảng trong DB nếu nó chưa tồn tại
model.Base.metadata.create_all(engine)


# app.add_middleware
