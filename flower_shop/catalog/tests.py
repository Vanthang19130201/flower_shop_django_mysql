from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Category, Product, ShopSettings
class StoreTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cat=Category.objects.create(name='Hoa sáp',slug='hoa-sap')
        cls.live=Product.objects.create(name='Hoa hồng',slug='hoa-hong',category=cls.cat,price=250000,original_price=300000)
        cls.hidden=Product.objects.create(name='Mẫu ẩn',slug='mau-an',category=cls.cat,price=200000,is_active=False)
    def test_catalog_and_hidden_product(self):
        response=self.client.get(reverse('home'))
        self.assertContains(response,'Hoa hồng')
        self.assertNotContains(response,'Mẫu ẩn')
        self.assertEqual(self.client.get(self.hidden.get_absolute_url()).status_code,404)
    def test_search_and_category(self):
        self.assertEqual(self.client.get('/',{'q':'không tồn tại'}).context['page_obj'].paginator.count,0)
        self.assertEqual(self.client.get('/',{'category':'hoa-sap','sale':'1'}).context['page_obj'].paginator.count,1)
    def test_admin_requires_authentication(self):
        self.assertEqual(self.client.get('/admin/catalog/product/add/').status_code,302)
    def test_invalid_discount_rejected(self):
        self.live.original_price=100
        with self.assertRaises(ValidationError): self.live.full_clean()
    def test_details_and_contact(self):
        ShopSettings.objects.create(name='Shop thử',zalo_url='https://zalo.me/0900000000')
        self.assertContains(self.client.get(self.live.get_absolute_url()),'https://zalo.me/0900000000')
    def test_html_is_escaped(self):
        self.live.description='<script>alert(1)</script>'
        self.live.save()
        response=self.client.get(self.live.get_absolute_url())
        self.assertNotContains(response,'<script>alert(1)</script>')
        self.assertContains(response,'&lt;script&gt;')
