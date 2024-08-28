from fastapi import FastAPI # pip install "fastapi[standard]"
import uvicorn
from fastapi.responses import FileResponse, HTMLResponse
from db import models
from db.database import engine
from router import user
from router import post


app = FastAPI()

# Thêm các router
app.include_router(user.router)
app.include_router(post.router)


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



if __name__ == "__main__":
    # Chạy file này bằng cách `python main.py`
    # sẽ lấy máy chạy file này làm máy chủ, các máy tính cùng dải mạng đều có thể truy cập API này
    # host = "0.0.0.0" cho phép các máy kết nối được với máy chủ (ping được tới máy chủ) đều có thể truy cập api
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # Hoặc gõ trực tiếp lệnh `fastapi dev main.py` để vào chế độ developer có thêm tham số --reload sẽ tự khởi động lại api khi thay đổi code 
    # Thêm tham số "--port 8080" để thay đổi cổng mở server
    # Hoặc gõ trực tiếp lệnh `fastapi run main.py` để vào chế độ lấy máy chạy làm server