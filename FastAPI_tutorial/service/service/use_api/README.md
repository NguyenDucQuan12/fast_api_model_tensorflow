Deploy FastAPI với Deta( deta.sh)  
Bước 1: Cài đặt Space CLI của deta tại đây `https://deta.space/docs/en/build/fundamentals/space-cli`  
Hoặc mở `Visual studio code`, mở dự án FastAPI và khởi động môi trường ảo, sau đó chạy lệnh sau trên terminal `iwr https://deta.space/assets/space-cli.ps1 -useb | iex`  
Bước 2: Đăng nhập vào deta  
Chạy lệnh `space login`  
Nếu lỗi `space : The term 'space' is not recognized as the name of a cmdlet,` thì khởi động lại visual và mở môi trường ảo  
Đăng nhập sẽ yêu cầu token để xác thực tài khoản, vào `setting` trong deta.sh để gettoken  
Sau khi đăng nhập thành công sẽ hiển thị `👍 Login Successful!` như bên dưới  
Bước 3: Tạo một dự án FastAPI, lưu ý không được đặt tên dự án là `venv`, hoặc `.venv` vì Spqce CLI sẽ tự động bỏ qua 2 thư mục có tên như này, nếu thư mục ảo có tên khác thì nhớ thêm nó vào tệp `.spaceignore`  
Bước 4: Tạo một dự án Space CLI mới bằng câu lệnh `space new`  
Lưu ý là phải mở ở thư mục gốc của dự án  