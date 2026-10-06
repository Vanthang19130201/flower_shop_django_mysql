"""Tạo .env dùng local, không ghi đè file có sẵn."""
from pathlib import Path
import secrets
root=Path(__file__).resolve().parent
path=root/'.env'
if path.exists():
    print('.env đã tồn tại, giữ nguyên.')
else:
    content=(root/'.env.example').read_text(encoding='utf-8')
    path.write_text(content.replace('SECRET_KEY=\n','SECRET_KEY='+secrets.token_urlsafe(48)+'\n'),encoding='utf-8')
    print('Đã tạo .env. Điền DB_PASSWORD của bạn trước khi chạy migrate.')
