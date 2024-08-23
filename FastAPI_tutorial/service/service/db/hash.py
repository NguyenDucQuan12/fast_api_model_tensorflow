# from passlib.context import CryptContext # pip install passlib

# pwd_cxt = CryptContext(schemes="bcrypt", deprecated = "auto")

# class Hash():

#     def bcrypt(password: str):
#         return pwd_cxt.hash(password)
    
#     def verify(hashed_password, plain_password):
#         return pwd_cxt.verify(plain_password, hashed_password)
"""
Không nên sử dụng passlib nữa bởi vì nó đã không còn cập nhật và sẽ gây ra lỗi: AttributeError: module 'bcrypt' has no attribute '__about__'
Chuyển sang sử dụng bcrypyt
"""  

import bcrypt  # pip install bcrypt


class Hash():

    """
    - **bcrypt**: Mã hóa mật khẩu người dùng
    - **verify**: Kiểm tra mật khẩu được cung cấp có trùng với mật khẩu đã mã hóa hay không
    """
    # Hash a password using bcrypt
    def bcrypt(password):
        """
        Mã hóa mật khẩu  
        Chuyển đổi dạng str sang byte để xử lý
        """
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password

    # Check if the provided password matches the stored password (hashed)
    def verify(plain_password, hashed_password):
        """
        Kiểm tra mật khẩu có trùng với mật khẩu đã mã hóa hay không  
        Chuyển đổi dạng str sang byte để xử lý
        """
        password_byte_enc = plain_password.encode('utf-8')
        hashed_password_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password = password_byte_enc , hashed_password = hashed_password_bytes)