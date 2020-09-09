def basket(request):
    if request.user.is_authenticated:
        basket = request.user.basket.select_related('product', 'product__category').all()
        # basket = request.user.basket.all()
    else:
        basket = []

    return {
        'basket': basket,
    }