import sys
import os
import datetime

today = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) #chua ngay thang nam cung voi gio phut giay
date_today = str(datetime.datetime.now().strftime("%d-%m-%y")) # chỉ chứa ngày tháng năm

# tạo thư mục nhật kí theo ngày tháng năm, nếu thư mục đã tồn tại thì không tạo nữa
save_dir_log = "service/log/"+ date_today
os.makedirs(save_dir_log, exist_ok=True)

log_file_path = save_dir_log +"/log.txt"
log_error_file_path = save_dir_log + "/error_log.txt"

# Ghi tất cả các thông báo bằng phương thức print vào file log, các lỗi xuất hiện vào file error_log
# Bởi vì khi đóng gói ứng dụng thì sẽ không có terminal hiển thị các thông tin này, vì vậy cần lưu vào file
# Với phương thức open thì sẽ tự động tạo file log nếu nó chưa tồn tại

# sys.stdout = open(log_error_file_path, encoding="utf-8", mode="a")
# sys.stderr = open(log_error_file_path, encoding="utf-8", mode="a")