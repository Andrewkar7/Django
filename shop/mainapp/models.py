from django.db import models


class ProductCategory(models.Model):
    name = models.CharField('имя категории', max_length=64)
    description = models.TextField('описание категории', blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True, db_index=True)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    category = models.ForeignKey(ProductCategory,
                                 on_delete=models.CASCADE,
                                 verbose_name='категория продукта')
    name = models.CharField('имя продукта', max_length=30)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField('краткое описание продукта', max_length=60, blank=True)
    description = models.TextField('описание продукта', blank=True)
    price = models.DecimalField('цена продукта', max_digits=4, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField('количество на складе', default=0)
    is_active = models.BooleanField(verbose_name='активна', default=True, db_index=True)

    def __str__(self):
        # return f"{self.name}({self.category.name})"
        return f"{self.name}"

    @staticmethod
    def get_active_items():
        return Product.objects.select_related().filter(category__is_active=True, is_active=True)
