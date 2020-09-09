from django.urls import path, re_path

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('product/', mainapp.product, name='product'),
    path('product/<int:page>/', mainapp.product, name='product_pagination'),

    # re_path(r'category/(?P<pk>\d+)/products/', mainapp.category_products, name='category_products'),
    path('category/<int:pk>/products/', mainapp.category_products, name='category_products'),
    path('category/<int:pk>/products/<int:page>/', mainapp.category_products, name='category_products_pagination'),

    path('product/<int:pk>/', mainapp.product_page, name='product_page'),

    path('product/detail/<int:pk>/async/', mainapp.product_detail_async),

    path('single/page/', mainapp.single_page, name='single_page'),
    path('checkout/', mainapp.checkout, name='checkout'),
]
