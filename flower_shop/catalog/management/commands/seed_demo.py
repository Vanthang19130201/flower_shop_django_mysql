from django.core.management.base import BaseCommand
from catalog.models import Category, Product, ShopSettings
class Command(BaseCommand):
    help = 'Tạo dữ liệu minh họa; không sửa dữ liệu đã tồn tại.'
    def handle(self,*args,**options):
        ShopSettings.objects.get_or_create(pk=1)
        for name,slug in [('Hoa sinh nhật','sinh-nhat'),('Hoa sáp','hoa-sap'),('Hoa tốt nghiệp','tot-nghiep'),('Hoa tình yêu','tinh-yeu')]:
            Category.objects.get_or_create(slug=slug,defaults={'name':name})
        samples=[('Nắng dịu','nang-diu','sinh-nhat',250000),('Lời thương','loi-thuong','hoa-sap',290000),('Chạm mùa hạ','cham-mua-ha','tot-nghiep',320000),('Hồng mơ','hong-mo','tinh-yeu',350000),('Một ngày vui','mot-ngay-vui','sinh-nhat',390000),('Gửi người thương','gui-nguoi-thuong','hoa-sap',420000),('Khởi đầu mới','khoi-dau-moi','tot-nghiep',450000),('Dịu dàng','diu-dang','tinh-yeu',490000)]
        for i,(name,slug,cat,price) in enumerate(samples):
            Product.objects.get_or_create(slug=slug,defaults={'name':name,'category':Category.objects.get(slug=cat),'price':price,'original_price':price+50000 if i%2==0 else None,'is_featured':i<4,'description':'Sản phẩm minh họa để thử giao diện. Hãy thay tên, ảnh, giá và mô tả bằng mẫu hoa thật của cửa hàng trước khi công khai.'})
        self.stdout.write(self.style.SUCCESS('Đã thêm dữ liệu minh họa. Không có tài khoản hoặc mật khẩu mặc định.'))
