# import tensorflow as tf
import uvicorn
import time
import logging
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, WebSocketDisconnect
from fastapi.websockets import WebSocket
from service.router import blog_get, blog_post, user
from service.router import article
from service.router import product
from service.router import file
from service.router import dependencies
from service.auth import authentication
from service.db import model
from service.templates import templates
from service.db.database import engine
from service.log.log import log_file_path
from service.client import html
from service.api_chat.message import save_message_to_file, load_messages_from_file, allowed_ips


"""
Tạo logging để lưu lại những thông tin ra với các tham số cụ thể như: thời gian, chế độ, tên file, hàm gọi, dòng code, id và tên thread, và tin nhắn
Lưu ý có thêm tham số: force = True bởi vì xung đột giữa các trình ghi nhật ký của các thư viện hoặc file
Nếu đối số từ khóa này được chỉ định là True, mọi trình xử lý hiện có được gắn vào bộ ghi nhật ký gốc sẽ bị 
xóa và đóng trước khi thực hiện cấu hình như được chỉ định bởi các đối số khác
Đối với file main sẽ dùng: logger = logging.getLogger()
Còn các file khác sẽ dùng: logger = logging.getLogger(__name__) thì sẽ tự động cùng lưu vào 1 file, cùng 1 định dạng
"""

logger = logging.getLogger()
# Dòng dưới sẽ ngăn chặn việc có những log không mong muốn từ thư viện PILLOW
# ví dụ: 2020-12-16 15:21:30,829 - DEBUG - PngImagePlugin - STREAM b'PLTE' 41 768
logging.getLogger("PIL.PngImagePlugin").propagate = False

logging.basicConfig(filename=log_file_path, filemode= 'a',
                    format='%(asctime)s %(levelname)s:\t %(filename)s: %(funcName)s()-Line: %(lineno)d\t id_thread: %(thread)d-thread_name: %(threadName)s\t message: %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p', encoding = 'utf-8', force=True)
logger.setLevel(logging.DEBUG)



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
app.include_router(dependencies.router)
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


clients = []

@app.get("/chat_with_people")
async def get():
    """
    Định dạng kiểu trả về trong đoạn hội thoại chat
    """
    return HTMLResponse(html)

@app.websocket("/chat_with_people")
async def websocket_endpoint(websocket: WebSocket):
    """
    Lưu ý tên endpoint **(`/chat_with_people`)** **`IP`** phải trùng với `ws = new WebSocket("ws://172.31.99.42:8000/chat_with_people");`  
    IP sẽ là địa chỉ IP của máy chủ server  
    Khi có người nào truy cập vào endpoint `http://IP:8000/chat_with_people` thì sẽ chấp nhận tất cả kết nối hoặc một số ip mới được kết nối  
    Chỉ những người đang truy cập vào endpoint mới có thể xem cuộc hội thoại và nhắn tin, những người vào sau thì không thể xem các tin nhắn trước
    """
    client_ip = websocket.client.host # https://github.com/encode/starlette/blob/5ee04ef9b1bc11dc14d299e6c855c9a3f7d5ff16/starlette/websockets.py#L20

    if client_ip not in allowed_ips:
        await websocket.close(code=1008)  # Đóng kết nối với mã 1008 - Policy Violation
        return 
    
    await websocket.accept()
    print(f"New connection accepted from {client_ip}")
    clients.append(websocket)
    
    # Gửi các tin nhắn cũ cho client khi kết nối
    old_messages = load_messages_from_file()
    for old_message in old_messages:
        await websocket.send_text(old_message.strip())

    try:
        while True:
            data = await websocket.receive_text()
            message = f"{client_ip}: {data}"  # Thêm thông tin người gửi
            # Lưu tin nhắn vào tệp
            save_message_to_file(message)

            # Gửi tin nhắn cho tất cả các client đang kết nối
            disconnected_clients = []

            for client in clients:
                try:
                    await client.send_text(message)
                except RuntimeError:
                    disconnected_clients.append(client)
            
            # Loại bỏ các client đã bị ngắt kết nối
            for dc_client in disconnected_clients:
                clients.remove(dc_client)

    except WebSocketDisconnect:
        clients.remove(websocket)
        print(f"Connection closed from {client_ip}")

# Tạo Bảng trong DB nếu nó chưa tồn tại
model.Base.metadata.create_all(engine)

## Một chức năng trung gian
@app.middleware("http")
async def add_middleware(request: Request, call_next):
    """
    Tính toán thời gian thực hiện của các `endpoint`  
    Để xem thời gian thực hiện của `endpoint` thì mở `console` bằng `F12` vào phần `Network`  
    Sau đó gọi API và quan sát kết quả trả về ở phần `Response Header` sẽ có mục `time_process`
    """
    start_time = time.time()
    response = await call_next(request)
    time_process = time.time()- start_time

    response.headers["time_process"]= str(time_process)
    return response

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
    # sẽ lấy máy chạy file này làm máy chủ, các máy tính cùng dải mạng đều có thể truy cập API này
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # Hoặc gõ trực tiếp lệnh `fastapi dev service\main.py --reload` để vào chế độ develop 
    # Hoặc gõ trực tiếp lệnh `fastapi run service\main.py --reload` để vào chế độ lấy máy chạy làm server