from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import F
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from adminapp.views import db_profile_by_type
from basketapp.models import Basket
from shop.settings import LOGIN_URL
from mainapp.models import Product


@login_required
def index(request):
    return render(request, 'basketapp/shopping_cart.html')


@login_required
def add_product(request, pk):
    if LOGIN_URL in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(
            # reverse('mainapp:product_page', args=[pk])
            reverse(
                'mainapp:product_page',
                kwargs={'pk': pk}
            )
        )

    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        # basket.quantity += 1
        # python code -> sql -> db -> python obj -> python logic -> sql -> db
        # F-object -> db level
        basket.quantity = F('quantity') + 1
        basket.save()
        db_profile_by_type(basket, 'UPDATE', connection.queries)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_product(request, pk):
    basket = get_object_or_404(Basket, pk=pk)
    basket.delete()
    return HttpResponseRedirect(reverse('basket:index'))


@login_required
def change(request, pk, quantity):
    # django_rest
    if request.is_ajax():
        basket = get_object_or_404(Basket, pk=pk)
        if quantity <= 0:
            basket.delete()
        else:
            basket.quantity = quantity
            basket.save()

        result = render_to_string(
            'basketapp/includes/inc__basket_list.html',
            request=request
        )

        return JsonResponse({'result': result})
        # return JsonResponse({
        #     'total_cost': basket.total_cost,
        #     'total_quantity': basket.total_quantity,
        #     'product_cost': basket.product_cost,
        # })


# @receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    print(f'pre save: {sender}')
    if instance.pk:
        instance.product.quantity -= instance.quantity - \
                                     sender.get_item(instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


# @receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    print(f'pre delete: {sender}')
    instance.product.quantity += instance.quantity
    instance.product.save()
