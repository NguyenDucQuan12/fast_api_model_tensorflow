import tensorflow as tf
from fastapi import FastAPI
from service.api.api import main_router


app = FastAPI(project_name = "TestAPI")

app.include_router(main_router)

# Tải mô hình 1 lần khi chạy server, các lần dự đoán sẽ không phải tải mô hình nữa
load_save_model = tf.keras.models.load_model(".FastAPI/service/core/logic/Malaria_model_save.keras")

@app.get("/")
def read_root():
    return {"Hello": "World"}
