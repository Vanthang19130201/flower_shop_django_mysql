# Flower Shop — Django + MySQL

Bản khởi đầu cho cửa hàng hoa nhỏ: trang khách, tìm kiếm/lọc/sắp xếp/phân trang, chi tiết sản phẩm, liên hệ đặt hoa, Django Admin. Cấu trúc danh mục và thẻ sản phẩm tham khảo FlowerCorner; nội dung và giao diện viết mới. Không dùng hình sản phẩm của website mẫu.

## 1. Mở project trong IntelliJ (Windows)

Ảnh của bạn đã có Python 3.11 và Project venv. Tạo Python project tên `flower_shop`, rồi chép toàn bộ nội dung thư mục trong ZIP vào project (manage.py nằm ngay ở thư mục gốc, không lồng flower_shop/flower_shop). Giữ lại .venv do IDE tạo. Hoặc giải nén, File → Open thư mục chứa manage.py rồi cấu hình Python interpreter.

Mở Terminal trong IDE. Kiểm tra:

```powershell
python --version
python -m pip --version
```

Nếu IDE chưa có môi trường ảo, tạo và dùng trực tiếp python của nó (không cần đổi ExecutionPolicy):

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Các lệnh `python` dưới đây phải chạy bằng interpreter của .venv. Nếu Terminal chưa kích hoạt venv, thay `python` bằng `.\.venv\Scripts\python.exe`.

```powershell
python -m pip install -r requirements.txt
python setup_local.py
```

## 2. Chuẩn bị MySQL

Cần MySQL Server đang chạy (khuyên dùng MySQL 8.4) và Workbench để quản lý. Workbench riêng lẻ không phải máy chủ.

Mở `database_setup.sql`, thay mật khẩu mẫu bằng mật khẩu riêng rồi chạy trong Workbench bằng tài khoản quản trị. Không gửi mật khẩu cho người khác. Nếu mật khẩu có dấu nháy đơn, cần escape đúng trong SQL.

Mở `.env` trong IDE và điền cùng thông tin:

```dotenv
DB_ENGINE=mysql
DB_NAME=flower_shop
DB_USER=flower_app
DB_PASSWORD="mat_khau_ban_da_dat"
DB_HOST=127.0.0.1
DB_PORT=3306
```

Giữ SECRET_KEY do setup_local.py tạo. Nếu MySQL dùng cổng khác, sửa DB_PORT.

## 3. Tạo bảng và tài khoản quản trị

```powershell
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Lệnh createsuperuser yêu cầu tự đặt tên và mật khẩu. Khi gõ mật khẩu trong terminal sẽ không hiện ký tự — đây là bình thường. Không có tài khoản mặc định.

- Cửa hàng: http://127.0.0.1:8000/
- Quản trị: http://127.0.0.1:8000/admin/

Trong admin: vào Thông tin cửa hàng để đổi tên, Zalo, Facebook, điện thoại, địa chỉ, giờ nhận đơn; vào Mẫu hoa để thêm ảnh và giá thật. Ảnh tối đa 5 MB. Nên dùng JPG/WebP, chiều rộng khoảng 1000–1400 px. Dữ liệu demo có giá minh họa và chưa có ảnh: thay hoặc xóa trước khi công khai. `seed_demo` chỉ thêm mẫu chưa tồn tại, không ghi đè sản phẩm đã sửa.

## 4. Các file chính

- config/settings.py: kết nối database và cấu hình.
- catalog/models.py: cấu trúc danh mục, sản phẩm, thông tin shop.
- catalog/admin.py: trang quản trị.
- catalog/views.py: lấy dữ liệu cho trang khách.
- templates/catalog/: HTML giao diện.
- static/catalog/style.css: màu sắc, bố cục desktop/điện thoại.
- media/: ảnh tải lên (tự sinh, không nằm trong mã nguồn).

## 5. Khi gặp lỗi

- `No module named django`: đang dùng sai interpreter hoặc chưa cài requirements.
- `Error loading MySQLdb`: chạy `python -m pip install mysqlclient`; trên Windows ưu tiên Python 3.11 64-bit. Nếu pip không có wheel phù hợp, cần công cụ build C++/thư viện client hoặc phiên bản Python có wheel; không sửa code để bỏ qua lỗi.
- `Can't connect ... 10061`: MySQL Server chưa chạy hoặc sai cổng.
- `Access denied`: kiểm tra user/password trong .env, quyền user và host.
- `Unknown database`: chạy database_setup.sql trước.
- `Table ... doesn't exist`: chạy migrate.
- Cổng 8000 bận: `python manage.py runserver 8001`.

## 6. Kiểm thử và giới hạn

```powershell
python manage.py check
python manage.py test
```

Django test tạo database test riêng, cần quyền tạo/xóa database test (user flower_app mặc định chỉ có quyền trên flower_shop). Có thể kiểm tra chức năng với SQLite: đặt biến môi trường DB_ENGINE=sqlite trong terminal test; không dùng như bằng chứng đã thử MySQL. Khi chạy thực tế vẫn dùng MySQL trong .env.

Bản này chưa có giỏ hàng, thanh toán trực tuyến hay lưu đơn hàng. Nút liên hệ mở đường dẫn shop đã cấu hình; khách gửi tên/mã mẫu qua tin nhắn. Chưa có thông tin liên hệ thì nút không xuất hiện.

## 7. Đưa lên mạng — bước tiếp theo

Đây là mã nguồn chạy local, chưa phải một website đã triển khai. Cần hosting chạy Python/Django, MySQL và nơi lưu ảnh bền vững; Cloudflare Pages không trực tiếp chạy máy chủ Django này. Domain/hosting miễn phí cần chọn riêng theo giới hạn dịch vụ.

Trước khi deploy: DEBUG=False, SECRET_KEY riêng, ALLOWED_HOSTS đúng domain, HTTPS, CSRF_TRUSTED_ORIGINS đúng origin; chạy `python manage.py check --deploy` và `collectstatic`. Dùng WSGI/ASGI server phù hợp, không dùng runserver. Cấu hình phục vụ static/media, sao lưu MySQL và ảnh. Nếu dùng reverse proxy, chỉ cấu hình tin cậy header HTTPS theo hướng dẫn hosting. Không upload .env hoặc database thật vào repo.

Tài liệu chính thức: https://docs.djangoproject.com/en/5.2/topics/install/ và https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
