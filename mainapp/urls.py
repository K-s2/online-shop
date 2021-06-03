from django.urls import path, include
from .views import test_view, ProductDetailVeiw

urlpatterns = [
    path('', test_view, name='base'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailVeiw.as_view(), name='product_detail')

]
