from fastapi import APIRouter, File, UploadFile
import shutil
from fastapi.responses import FileResponse
import os
from fastapi import HTTPException

router = APIRouter(
    prefix="/file",
    tags=["file"]
)


@router.post("/file")
def get_file(file: bytes = File(...)):
    """
    Nhận file từ người dùng tải lên  
    Các file này sẽ được lưu trực tiếp vào RAM nên chỉ áp dụng cho các file nhỏ như **txt**  
    Nếu không bộ nhớ sẽ đầy và gây ra lỗi
    """
    content = file.decode("utf-8")
    lines = content.split("\n")
    return {
        "line": lines
    }

@router.post("/upload_file")
def get_upload_file(file: UploadFile = File(...)):
    """
    Nhận file từ người dùng tải lên  
    Lưu ý file có thể bị ghi đè nếu nó trùng tên, vì vậy hãy đặt tên file lưu trữ chứa giờ phút giây để có thể không trùng  
    - **path** là đường dẫn sẽ lưu file ở đâu trên máy cục bộ của mình  
    - Sử dụng hàm **shutil** để copy file 
    """
    path = f"files/{file.filename}"
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {
        "filename": path,
        "type": file.content_type
    }

@router.get("/download/{name}", response_class= FileResponse )
def download_file_from_browser(name: str):
    """
    API tự động tải xuống tệp tin từ server bằng trình duyệt khi dán `endpoint` vào trình duyệt  
    Yêu cầu trạng thái phản hồi là **response_class= FileResponse**  
    - **name**: là tệp tin mà người dùng muốn tải, nó yêu cầu cả đuôi như cat.png, requirements.txt
    """
    path = f"files/{name}"

    # Kiểm tra xem tệp có tồn tại không
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Thiết lập tiêu đề để buộc trình duyệt tải xuống tệp
    headers = {
        "Content-Disposition": f"attachment; filename={name}"
    }
    
    return FileResponse(path=path, headers= headers)

@router.get("/view/{name}", response_class= FileResponse )
def get_file(name: str):
    """
    API cho phép người dùng tải xuống tệp tin từ server  
    Yêu cầu trạng thái phản hồi là **response_class= FileResponse**  
    - **name**: là tệp tin mà người dùng muốn tải, nó yêu cầu cả đuôi như cat.png, requirements.txt
    ## Ví dụ
    ```python
    import requests

    # URL của API mà bạn muốn tải xuống tệp
    url_view_file = "http://localhost:8000/file/view/cat.png"

    # Gửi yêu cầu GET để tải xuống tệp
    response = requests.get(url_view_file)

    # Kiểm tra nếu yêu cầu thành công
    if response.status_code == 200:
        # Lưu tệp vào đĩa
        with open("downloaded_cat.png", "wb") as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
    ```
    """

    path = f"files/{name}"

    # Kiểm tra xem tệp có tồn tại không
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return path