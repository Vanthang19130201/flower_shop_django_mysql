import uuid
from pathlib import Path
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.urls import reverse

def image_path(instance, filename):
    return f'flowers/{uuid.uuid4().hex}{Path(filename).suffix.lower()}'

def image_limit(value):
    if value.size > 5 * 1024 * 1024:
        raise ValidationError('Ảnh tối đa 5 MB.')

class Category(models.Model):
    name = models.CharField('Tên danh mục', max_length=100)
    slug = models.SlugField('Đường dẫn', unique=True)
    class Meta:
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Danh mục'
        ordering = ['name']
    def __str__(self): return self.name

class Product(models.Model):
    name = models.CharField('Tên mẫu hoa', max_length=150)
    slug = models.SlugField('Đường dẫn', unique=True)
    category = models.ForeignKey(Category, verbose_name='Danh mục', on_delete=models.PROTECT, related_name='products')
    description = models.TextField('Mô tả', blank=True)
    price = models.DecimalField('Giá bán (đ)', max_digits=12, decimal_places=0, validators=[MinValueValidator(0)])
    original_price = models.DecimalField('Giá trước giảm (đ)', max_digits=12, decimal_places=0, blank=True, null=True, validators=[MinValueValidator(0)])
    image = models.ImageField('Ảnh sản phẩm', upload_to=image_path, blank=True, validators=[image_limit])
    is_active = models.BooleanField('Hiển thị trên cửa hàng', default=True)
    is_available = models.BooleanField('Đang nhận đặt', default=True)
    is_featured = models.BooleanField('Mẫu nổi bật', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Mẫu hoa'
        verbose_name_plural = 'Mẫu hoa'
        ordering = ['-created_at']
        constraints = [models.CheckConstraint(condition=models.Q(price__gte=0), name='price_nonnegative'), models.CheckConstraint(condition=models.Q(original_price__isnull=True)|models.Q(original_price__gte=models.F('price')), name='original_price_valid')]
    def clean(self):
        if self.original_price is not None and self.price is not None and self.original_price < self.price:
            raise ValidationError({'original_price':'Giá trước giảm phải lớn hơn hoặc bằng giá bán.'})
    def __str__(self): return self.name
    def get_absolute_url(self): return reverse('product', args=[self.slug])
    @property
    def discount(self):
        if self.original_price and self.original_price > self.price:
            return round((self.original_price-self.price)*100/self.original_price)
        return 0

class ShopSettings(models.Model):
    name = models.CharField('Tên cửa hàng', max_length=100, default='Tiệm Hoa')
    tagline = models.CharField('Thông điệp', max_length=160, default='Gửi hoa, gửi điều thương.')
    about = models.TextField('Giới thiệu', default='Một bó hoa nhỏ cho những điều đáng nhớ. Chọn mẫu bạn thích và nhắn cho tiệm để cùng chuẩn bị món quà phù hợp.')
    phone = models.CharField('Điện thoại', max_length=16, blank=True, validators=[RegexValidator(r'^\+?[0-9]{9,15}$','Nhập 9–15 chữ số, có thể bắt đầu bằng +.')])
    zalo_url = models.URLField('Đường dẫn Zalo', blank=True)
    facebook_url = models.URLField('Đường dẫn Facebook / Messenger', blank=True)
    address = models.CharField('Địa chỉ / khu vực phục vụ', max_length=250, blank=True)
    hours = models.CharField('Giờ nhận đơn', max_length=100, blank=True)
    ordering_guide = models.TextField('Hướng dẫn đặt hoa', default='1. Chọn mẫu hoa bạn thích.\n2. Nhắn cho tiệm mã mẫu, ngân sách và ngày nhận.\n3. Tiệm xác nhận mẫu, phí giao và cách thanh toán trước khi thực hiện.')
    care_guide = models.TextField('Hướng dẫn bảo quản', default='Hoa sáp: giữ nơi khô ráo, tránh nước và ánh nắng trực tiếp.\nHoa tươi: thay nước sạch, cắt gốc và để nơi thoáng mát.')
    class Meta:
        verbose_name = 'Thông tin cửa hàng'
        verbose_name_plural = 'Thông tin cửa hàng'
    def save(self,*args,**kwargs):
        self.pk = 1
        super().save(*args,**kwargs)
    def __str__(self): return self.name
