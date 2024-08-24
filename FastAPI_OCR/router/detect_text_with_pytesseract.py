from fastapi import APIRouter, File, UploadFile
import shutil
from fastapi import HTTPException
import pytesseract
from assets.model.model import get_language_for_ocr_pytesseract_model, language_trans

"""
pytesseract nhận diện tốt cho tiếng Việt
"""
router = APIRouter(
    prefix="/pytesseract",
    tags=["pytesseract"]
)

@router.post("/detect/{language}")
def ocr(language: str = "vie", image: UploadFile = File(...)):
    """
    Tải hình ảnh có chứa văn bản và nhận về các văn bản  
    -- **language**: ngôn ngữ văn bản, có thể `vie : Tiếng Việt`, `jpn: Tiếng Nhật` hoặc `vie+jpn: là văn bản bao gồm cả tiếng Việt và tiếng Nhật`  
    Để sử dụng trong code làm như sau  
    ## Ví dụ  
    ```python
    import requests

    # Địa chỉ URL của API OCR
    url = "http://10.239.2.91:8000/pytesseract/detect/vie # Địa chỉ ip phù hợp với server đang chạy API

    # Đường dẫn tới tệp hình ảnh mà bạn muốn OCR
    image_path = "path/to/your/image.jpg"  # Thay thế bằng đường dẫn tới tệp hình ảnh của bạn

    # Mở tệp hình ảnh ở chế độ đọc nhị phân
    with open(image_path, "rb") as image_file:
        # Tạo dữ liệu tệp để gửi với yêu cầu
        files = {"image": image_file}
        # Gửi yêu cầu POST tới API
        response = requests.post(url, files=files)

    # Kiểm tra phản hồi
    if response.status_code == 200:
        # In ra văn bản đã được OCR từ hình ảnh
        print("OCR Result:", response.text)
    else:
        print("Failed to perform OCR. Status code:", response.status_code)
        print("Response:", response.text)
    ```
    """

    if not language in language_trans:
        raise HTTPException(status_code=400, detail= f"Language accept: {language_trans}")
    
    language = get_language_for_ocr_pytesseract_model(language= language)

    filepath = "txtFile"
    with open(filepath, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    result_text = pytesseract.image_to_string(filepath, lang=language) #lang="vie", lang="eng", lang="eng+jpn"

    # Tách chuỗi thành các đoạn nhỏ hơn khi gặp dấu phân cách '\n'
    result_text = result_text.split('\n')
    return {
        "language": language,
        "result": result_text
    }