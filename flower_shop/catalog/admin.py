from django.contrib import admin
from .models import Category, Product, ShopSettings
admin.site.site_header = 'Quản trị cửa hàng hoa'
admin.site.site_title = 'Quản trị'
admin.site.index_title = 'Quản lý cửa hàng'
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    search_fields = ['name']
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','category','price','is_active','is_available','is_featured']
    list_filter = ['category','is_active','is_available','is_featured']
    list_editable = ['price','is_active','is_available','is_featured']
    search_fields = ['name','description']
    prepopulated_fields = {'slug':('name',)}
    readonly_fields = ['created_at']
@admin.register(ShopSettings)
class ShopSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self,request):
        return super().has_add_permission(request) and not ShopSettings.objects.exists()
    def has_delete_permission(self,request,obj=None): return False
