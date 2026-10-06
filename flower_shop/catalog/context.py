from .models import Category, ShopSettings
def shop_context(request):
    return {'shop':ShopSettings.objects.first() or ShopSettings(), 'categories':Category.objects.all()}
