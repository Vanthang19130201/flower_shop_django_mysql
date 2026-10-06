from django.urls import path
from . import views
urlpatterns = [path('',views.home,name='home'),path('hoa/<slug:slug>/',views.product,name='product')]
