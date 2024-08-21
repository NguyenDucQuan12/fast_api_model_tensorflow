from fastapi import APIRouter, File


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