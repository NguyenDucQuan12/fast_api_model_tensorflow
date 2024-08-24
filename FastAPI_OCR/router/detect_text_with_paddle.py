# pip install paddlepaddle-gpu # for CUDA11
# python -m pip install paddlepaddle
# pip install "paddleocr>=2.0.1" # Recommend to use version 2.0.1+
from paddleocr import draw_ocr
from fastapi import APIRouter, File, UploadFile
import shutil
from fastapi import HTTPException
from assets.model.model import get_ocr_paddle_model, language_trans


"""
Để dùng tốt PaddleOCR cho nhận diện và đọc chữ thì phải chọn đúng ngôn ngữ trong mục `lang` và đường dẫn `rec_model_dir`, `det_model_dir`, `cls_model_dir`  
PaddleOCR hỗ trợ tốt ngôn ngữ Trung, Tiếng Anh, Nhật, ... https://paddlepaddle.github.io/PaddleOCR/en/ppocr/blog/multi_languages.html#5-support-languages-and-abbreviations  
Nếu muốn tải modle ngôn ngữ khác thì chỉ cần thay đổi ngôn ngữ với tham số `lang = "chữ viết tắt"`, và cung cấp 3 đường dẫn mới phù hợp với ngôn ngữ đó để model tải về lưu vào đó, sau này chạy thì không cần phải tải lại nữa  
Lưu ý dùng tiếng Việt thì sử dụng `pytesseract`  
"""
router = APIRouter(
    prefix="/paddleocr",
    tags=["paddleocr"]
)


@router.post("/detect/{lang}")
def get_upload_file(lang: str, image: UploadFile = File(...)):
    """
    """
    result_text = []

    if not lang in language_trans:
        raise HTTPException(status_code=400, detail= f"Language accept: {language_trans}")
    
    ocrEngine = get_ocr_paddle_model(language= lang)
    
    filepath = "txtFile"
    with open(filepath, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    result= ocrEngine.ocr(filepath, cls=True)[0]

    for number, line in enumerate(result):
            result_text.append(f"line {number}: {line[1][0]}")
    
    return {
        "language": lang,
        "result": result_text
    }




if __name__ == "__main__":

    img_path = "assets/image_test/text_image_japan.png"
    ocrEngine = get_ocr_paddle_model(language= "vietnam")
    result= ocrEngine.ocr(img_path, cls=True)[0]

    # draw result
    from PIL import Image # pip install pillow
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='assets/fonts/simfang.ttf')
    im_show = Image.fromarray(im_show)
    im_show.save("result.jpg")
    im_show.show()