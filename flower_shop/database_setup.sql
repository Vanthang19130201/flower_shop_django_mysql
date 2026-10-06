-- Chạy bằng tài khoản quản trị trong MySQL Workbench.
-- Thay REPLACE_WITH_YOUR_PASSWORD trước khi chạy; không dùng mật khẩu này nguyên văn.
CREATE DATABASE IF NOT EXISTS flower_shop CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'flower_app'@'localhost' IDENTIFIED BY 'REPLACE_WITH_YOUR_PASSWORD';
GRANT ALL PRIVILEGES ON flower_shop.* TO 'flower_app'@'localhost';
-- Nếu user đã tồn tại, CREATE USER không đổi mật khẩu. Dùng mật khẩu đã đặt cho user đó.
