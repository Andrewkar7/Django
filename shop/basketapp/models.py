from django.utils.functional import cached_property

from django.db import models

from authapp.models import ShopUser
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('количество', default=0)
    add_datetime = models.DateTimeField('время', auto_now_add=True)

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related().all()

    @property
    def product_cost(self):
        "return cost of all products this type"
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        "return total quantity for user"
        return sum(map(lambda x: x.quantity, self.get_items_cached))

    @property
    def total_cost(self):
        "return total cost for user"
        return sum(map(lambda x: x.product_cost, self.get_items_cached))

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)
