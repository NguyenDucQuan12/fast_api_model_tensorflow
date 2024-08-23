import os

# Tệp để lưu trữ tin nhắn
MESSAGE_FILE = "chat_messages.txt"

# Danh sách các địa chỉ IP được phép kết nối
allowed_ips = ["127.0.0.1", "172.31.99.129", "172.31.99.42", "10.239.2.91"]

def save_message_to_file(message):
    with open(MESSAGE_FILE, "a", encoding="utf-8") as file:
        file.write(message + "\n")

def load_messages_from_file():
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, "r") as file:
            return file.readlines()
    return []
