from fastapi import FastAPI # pip install "fastapi[standard]"
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from db import models
from db.database import engine
from router import user
from router import post
from router import comment
from auth import authentication


app = FastAPI()

# Thêm các router
app.include_router(user.router)
app.include_router(post.router)
app.include_router(authentication.router)
app.include_router(comment.router)


# Serve the favicon
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("files/favicon.ico")

# Trang chủ
@app.get("/")
def root():
    return "Hello World"

# Tạo CSDL
models.Base.metadata.create_all(engine)

# Truy cập các tài nguyên trong thư mục `files/images` bằng địa chỉ http://127.0.0.1:8000/files/images/tenfile.đuôi
app.mount("/files/images", StaticFiles(directory = "files/images"), name= "images")


# Cho phép các máy chủ, API khác chạy trên cùng 1 máy tính truy cập tài nguyên vào API này
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

if __name__ == "__main__":
    # Chạy file này bằng cách `python main.py`
    # sẽ lấy máy chạy file này làm máy chủ, các máy tính cùng dải mạng đều có thể truy cập API này
    # host = "0.0.0.0" cho phép các máy kết nối được với máy chủ (ping được tới máy chủ) đều có thể truy cập api
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # Hoặc gõ trực tiếp lệnh `fastapi dev main.py` để vào chế độ developer có thêm tham số --reload sẽ tự khởi động lại api khi thay đổi code 
    # Thêm tham số "--port 8080" để thay đổi cổng mở server
    # Hoặc gõ trực tiếp lệnh `fastapi run main.py` để vào chế độ lấy máy chạy làm server