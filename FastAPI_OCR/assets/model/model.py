from paddleocr import PaddleOCR

# Danh sách các ngôn ngữ
language_trans = ["vietnam", "japan", "english", "china"]

# Khởi tạo các mô hình Paddle OCR cho từng ngôn ngữ
ocr_paddle_models = {
    "japan": PaddleOCR(
        use_angle_cls=False,
        lang='japan',  # "en", "japan", "vi", "ch"
        show_log=False,
        use_gpu=False,
        rec_model_dir="assets/model/japan/rec",
        det_model_dir="assets/model/japan/det",
        cls_model_dir="assets/model/japan/cls"
    ),
    "vietnam": PaddleOCR(
        use_angle_cls=False,
        lang='vi',  # "en", "japan", "vi", "ch"
        show_log=False,
        use_gpu=False,
        rec_model_dir="assets/model/vietnam/rec",
        det_model_dir="assets/model/vietnam/det",
        cls_model_dir="assets/model/vietnam/cls"
    ),
    "english": PaddleOCR(
        use_angle_cls=False,
        lang='en',  # "en", "japan", "vi", "ch"
        show_log=False,
        use_gpu=False,
        rec_model_dir="assets/model/english/rec",
        det_model_dir="assets/model/english/det",
        cls_model_dir="assets/model/english/cls"
    ),
    "china": PaddleOCR(
        use_angle_cls=False,
        lang='ch',  # "en", "japan", "vi", "ch"
        show_log=False,
        use_gpu=False,
        rec_model_dir="assets/model/china/rec",
        det_model_dir="assets/model/china/det",
        cls_model_dir="assets/model/china/cls"
    )
}

def get_ocr_paddle_model(language: str):
    """
    Trả về mô hình OCR tương ứng dựa trên ngôn ngữ.
    Nếu ngôn ngữ không hợp lệ, trả về None.
    """
    return ocr_paddle_models.get(language)


ocr_pytesseract_models = {
    "japan": "jpn",
    "vietnam": "vie",
    "english": "eng",
    "japan_english": "eng+jpn"
}

def get_language_for_ocr_pytesseract_model(language: str):
    """
    Trả về mô hình OCR tương ứng dựa trên ngôn ngữ.
    Nếu ngôn ngữ không hợp lệ, trả về None.
    """
    return ocr_pytesseract_models.get(language)