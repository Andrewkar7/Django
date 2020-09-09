from django.test import TestCase

from mainapp.models import Product, ProductCategory


class ProductsTestCase(TestCase):
    def setUp(self):
        category = ProductCategory.objects.create(name="сапоги")
        self.product_1 = Product.objects.create(
            name="сапог 1",
            category=category,
            price=15,
            quantity=150
        )
        self.product_2 = Product.objects.create(
            name="сапог 2",
            category=category,
            price=18,
            quantity=125,
            is_active=False
        )
        self.product_3 = Product.objects.create(
            name="сапог 3",
            category=category,
            price=22,
            quantity=115
        )

    def test_product_get(self):
        product_1 = Product.objects.get(name="сапог 1")
        product_2 = Product.objects.get(name="сапог 2")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_print(self):
        product_1 = Product.objects.get(name="сапог 1")
        product_2 = Product.objects.get(name="сапог 2")
        self.assertEqual(str(product_1), 'сапог 1')
        self.assertEqual(str(product_2), 'сапог 2')

    def test_product_get_items(self):
        product_1 = Product.objects.get(name="сапог 1")
        product_3 = Product.objects.get(name="сапог 3")
        products = Product.get_active_items()

        self.assertEqual(list(products), [product_1, product_3])
