from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, F
from .models import Product

def home(request):
    products = Product.objects.filter(is_active=True).select_related('category')
    q = request.GET.get('q','').strip()[:150]
    category = request.GET.get('category','')
    sort = request.GET.get('sort','newest')
    if q: products = products.filter(Q(name__icontains=q)|Q(description__icontains=q))
    if category: products = products.filter(category__slug=category)
    if request.GET.get('sale') == '1': products = products.filter(original_price__gt=F('price'))
    products = products.order_by({'price_up':'price','price_down':'-price','newest':'-created_at'}.get(sort,'-created_at'), 'pk')
    params = request.GET.copy()
    params.pop('page',None)
    return render(request,'catalog/home.html',{'page_obj':Paginator(products,12).get_page(request.GET.get('page')), 'q':q,'selected_category':category,'sort':sort,'querystring':params.urlencode(),'filtered':bool(q or category or request.GET.get('sale')), 'featured':Product.objects.filter(is_active=True,is_featured=True)[:4]})

def product(request,slug):
    item = get_object_or_404(Product.objects.select_related('category'),slug=slug,is_active=True)
    related = Product.objects.filter(is_active=True,category=item.category).exclude(pk=item.pk)[:4]
    return render(request,'catalog/product.html',{'product':item,'related':related})
