# import tensorflow as tf
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from service.router import blog_get, blog_post, user
from service.router import article
from service.router import product
from service.router import file
from service.auth import authentication
from service.db import model
from service.templates import templates
from service.db.database import engine
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(project_name = "TestAPI")

app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(blog_post.router)
app.include_router(product.router)
app.include_router(article.router)
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(templates.router)
# app.include_router(main_router)

"""
Cho phép truy cập file tĩnh trong API bằng thư viện **aiofiles**  
Cần cài đặt thư viện này và không cần import **pip install aiofiles**  
Cho phép truy cập các file ở trong thư mục **files** với đường dẫn **http://127.0.0.1:8000/files/tenfile.đuôi**  
Đường dẫn có thể thay đổi nếu chạy thật thì thay thế bằng IP của máy chủ
"""
app.mount("/files", StaticFiles(directory = "files"), name = "files")

app.mount("/templates/static", StaticFiles(directory = "service/templates/static"), name = "static")


# Serve the favicon
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("files/favicon.ico")


@app.get("/")
def read_root():
    return {"Message": "World"}

# Tạo Bảng trong DB nếu nó chưa tồn tại
model.Base.metadata.create_all(engine)

"""
Cho phép các trang web, app, api trên cùng 1 máy tính có thể truy cập đến api này  
Mặc định các api trên cùng 1 máy không thể chia sẻ tài nguyên cho nhau  
Điều này phục vụ cho mục đích test, vì không thể lúc nào cũng có sẵn 2 máy tính khác nhau để test
"""
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
    # Chạy file này bằng cách `python service\main.py`
    # sẽ cho phép các máy có quyền truy cập API này
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # Hoặc gõ trực tiếp lệnh `fastapi dev service\main.py --reload`