from fastapi import FastAPI
import pytesseract
import uvicorn
from router import detect_text_with_paddle
from router import detect_text_with_pytesseract



app = FastAPI()

app.include_router(detect_text_with_paddle.router)
app.include_router(detect_text_with_pytesseract.router)

# install exe: https://github.com/UB-Mannheim/tesseract/wiki 
# Trong quá trình cài đặt nhớ chọn thêm ngôn ngữ: Vietnames, ... nếu không thì tải về tại: https://tesseract-ocr.github.io/tessdoc/Data-Files.html
# Sau đó copyfile và paste vào: C:\Program Files\Tesseract-OCR\tessdata

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



@app.post("")
def root():
    return {
        "Quân IT": "Nhận diện ngôn ngữ từ hình ảnh"
    }




if __name__ == "__main__":
    # Chạy file này bằng cách `python service\main.py`
    # sẽ lấy máy chạy file này làm máy chủ, các máy tính cùng dải mạng đều có thể truy cập API này
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # Hoặc gõ trực tiếp lệnh `fastapi dev service\main.py --reload` để vào chế độ develop 
    # Hoặc gõ trực tiếp lệnh `fastapi run service\main.py --reload` để vào chế độ lấy máy chạy làm server


"""
import os
import cv2
from paddleocr import PPStructure,draw_structure_result,save_structure_res
from PIL import Image

table_engine = PPStructure(show_log=True, image_orientation=True)

save_folder = './output'
img_path = './334352202-c065007d-96b3-4a30-ab4d-42be47ec3ee8.png'
img = cv2.imread(img_path)
result = table_engine(img)
save_structure_res(result, save_folder,os.path.basename(img_path).split('.')[0])

for line in result:
    line.pop('img')
    print(line)

font_path = 'doc/fonts/simfang.ttf' # PaddleOCR下提供字体包
image = Image.open(img_path).convert('RGB')
im_show = draw_structure_result(image, result,font_path=font_path)
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')
"""
