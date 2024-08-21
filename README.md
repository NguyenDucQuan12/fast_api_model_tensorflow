# fast_api_model_tensorflow
# Tạo môi trường ảo có tên là .FastAPI  
Sau đó cài đặt các thư viện theo mục `requirements.txt` bằng câu lệnh `pip install -r requirements.txt`  
copy các file vào thư mục `.FastAPI`  
### Chạy API
`fastapi dev .FastAPI\service\main.py --reload` tham số `--reload` sẽ tự động khởi động lại API khi có sự thay đổi code  
Hai trang web kiểm tra API  
```
Serving at: http://127.0.0.1:8000  
API docs: http://127.0.0.1:8000/docs     
```
Để chạy API trong môi trường thật thì sử dụng câu lệnh `fastapi run .FastAPI\service\main.py`  
Vào máy khác và nhập đường link để thử API bằng cách `http://IP:8000/endpoint`  
