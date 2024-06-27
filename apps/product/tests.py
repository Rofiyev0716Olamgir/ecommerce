from django.test import TestCase
# from django.conf import settings
from django.urls import reverse
# from .models import Product, Category
from .models import Product, Category, Tag, ProductImage
from django.core.files.uploadedfile import SimpleUploadedFile


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Kategoriyalar va teglar yaratamiz
        category = Category.objects.create(name='Electronics')
        tag1 = Tag.objects.create(name='New')
        tag2 = Tag.objects.create(name='Sale')

        # Mahsulot yaratamiz
        product = Product.objects.create(
            name='Laptop',
            C=category,
            price=999.99,
            discount=10,
            description='A powerful laptop.',
            views=100,
            sold_count=50
        )
        product.tags.add(tag1, tag2)

        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        ProductImage.objects.create(product=product, image=image)

    def test_product_str(self):
        product = Product.objects.get(id=1)
        self.assertEqual(str(product), 'Laptop')

    def test_product_average_rank(self):
        product = Product.objects.get(id=1)
        self.assertEqual(product.average_rank, 1)

    def test_product_get_quantity(self):
        product = Product.objects.get(id=1)
        self.assertEqual(product.get_quantity, 0)

    def test_product_get_likes_count(self):
        product = Product.objects.get(id=1)
        self.assertEqual(product.get_likes_count, 0)

    def test_product_is_available(self):
        product = Product.objects.get(id=1)
        self.assertFalse(product.is_available)

    def test_product_image_str(self):
        product_image = ProductImage.objects.get(id=1)
        self.assertEqual(str(product_image), 'Laptop')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_list.html')

    def test_view_lists_all_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['product_list']), 1)
        self.assertContains(response, 'Laptop')

    def test_product_tags(self):
        product = Product.objects.get(id=1)
        self.assertEqual(product.tags.count(), 2)

    def test_product_category(self):
        product = Product.objects.get(id=1)
        self.assertEqual(product.C.name, 'Electronics')

# class ProductListViewTests(TestCase):
#
#     pass

    # def test_view_uses_correct_template(self):
    #     url = reverse('product-list')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'product_list.html')

    # def test_product_list_view(self):
    #     response = Product.objects.create(name='Product 1', price=,)
    #     self.assertEqual(response.status_code, 200)

    # def test_product_create(self):
    #     product = Product.objects.create(name='test', )
    #     self.assertEqual(product.name, 'test')
    #
    # def test_product_count(self):
    #     product = Product.objects.create(name='test', content='test')
    #     products = Product.objects.all()
    #     self.assertEqual(products.count(), 'test')
    #
    # @classmethod
    # def setUpTestData(cls):
    #     # Test uchun ba'zi mahsulotlar yaratamiz
    #     number_of_products = 13
    #     for product_id in range(number_of_products):
    #         Product.objects.create(
    #             name=f'Product {product_id}',
    #             price=10.99,
    #             description=f'Description for product {product_id}',
    #         )
    #
    # def test_view_url_exists_at_desired_location(self):
    #     response = self.client.get('/products/')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_view_url_accessible_by_name(self):
    #     response = self.client.get(reverse('product_list'))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_view_uses_correct_template(self):
    #     response = self.client.get(reverse('product_list'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'shop/product_list.html')
    #
    # def test_pagination_is_five(self):
    #     response = self.client.get(reverse('product_list'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('is_paginated' in response.context)
    #     self.assertTrue(response.context['is_paginated'] is True)
    #     self.assertEqual(len(response.context['product_list']), 5)
    #
    # def test_lists_all_products(self):
    #     pass


