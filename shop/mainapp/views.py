import random

from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page

from mainapp.models import ProductCategory, Product
from shop.settings import LOW_CACHE


# from doc
def get_category(pk):
    if LOW_CACHE:
        key = f'productcategory_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True,
                                              category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True,
                                      category__is_active=True).order_by('price')


def get_products_in_productcategory(pk):
    if LOW_CACHE:
        key = f'products_in_productcategory_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


# native
def get_hot_product():
    return random.choice(Product.objects.filter(is_active=True))


def get_menu():
    if LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def index(request):
    feature__boxes = [
        {
            'title': 'Free delivery',
            'img': 'img/delivery.png',
        },
        {
            'title': 'Sales & discounts',
            'img': 'img/discount.png',
        },
        {
            'title': 'Quality assurance',
            'img': 'img/quality.png',
        },
    ]

    showcase__conteiner = [
        {
            'product_img': 'img/products/men_product_00001.jpg',
        },
        {
            'product_img': 'img/products/women_product_00005.jpg',
        },
        {
            'product_img': 'img/products/men_product_00002.jpg',
        },
        {
            'product_img': 'img/products/women_product_00006.jpg',
        },
        {
            'product_img': 'img/products/women_product_00007.jpg',
        },
        {
            'product_img': 'img/products/men_product_00003.jpg',
        },
        {
            'product_img': 'img/products/men_product_00004.jpg',
        },
        {
            'product_img': 'img/products/men_product_00005.jpg',
        },
    ]

    context = {
        'page_title': 'home',
        'feature__boxes': feature__boxes,
        'showcase__conteiner': showcase__conteiner,
    }
    return render(request, 'mainapp/index.html', context)


def product(request, page=1):
    products = Product.objects.filter(is_active=True)

    products_paginator = Paginator(products, 3)
    try:
        products = products_paginator.page(page)
    except PageNotAnInteger:
        products = products_paginator.page(1)
    except EmptyPage:
        products = products_paginator.page(products_paginator.num_pages)

    feature__boxes = [
        {
            'title': 'Free delivery',
            'img': 'img/delivery.png',
        },
        {
            'title': 'Sales & discounts',
            'img': 'img/discount.png',
        },
        {
            'title': 'Quality assurance',
            'img': 'img/quality.png',
        },
    ]

    context = {
        'page_title': 'products',
        'feature__boxes': feature__boxes,
        'categories': get_menu(),
        'products': products,
    }
    return render(request, 'mainapp/product.html', context)


def category_products(request, pk, page=1):
    if pk == '0':
        category = {'pk': 0, 'name': 'все'}
        products = get_products()
    else:
        category = get_category(pk)
        products = get_products_in_productcategory(pk)

    products_paginator = Paginator(products, 3)
    try:
        products = products_paginator.page(page)
    except PageNotAnInteger:
        products = products_paginator.page(1)
    except EmptyPage:
        products = products_paginator.page(products_paginator.num_pages)

    feature__boxes = [
        {
            'title': 'Free delivery',
            'img': 'img/delivery.png',
        },
        {
            'title': 'Sales & discounts',
            'img': 'img/discount.png',
        },
        {
            'title': 'Quality assurance',
            'img': 'img/quality.png',
        },
    ]

    context = {
        'page_title': 'category of products',
        'categories': get_menu(),
        'feature__boxes': feature__boxes,
        'category': category,
        'products': products,

    }
    return render(request, 'mainapp/category_products.html', context)


def product_page(request, pk):
    product = Product.objects.all()
    context = {
        'page_title': 'products',
        'categories': get_menu(),
        'category': product.category,
        'product': product,
    }
    return render(request, 'mainapp/product_page.html', context)


def single_page(request):
    products = Product.objects.all()
    hot_product = get_hot_product()

    same_products = hot_product.category.product_set.filter(is_active=True).select_related().exclude(pk=hot_product.pk)

    context = {
        'page_title': 'single page',
        'products': products,
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request, 'mainapp/single_page.html', context)


def checkout(request):
    context = {
        'page_title': 'checkout',
    }
    return render(request, 'mainapp/checkout.html', context)


def product_detail_async(request, pk):
    if request.is_ajax():
        try:
            product = get_product(pk)
            return JsonResponse({
                'product_price': product.price,
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            })
