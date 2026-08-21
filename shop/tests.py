from decimal import Decimal
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from shop.models import Category, Product


class ShopModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Ноутбуки', slug='laptops')
        self.product = Product.objects.create(
            category=self.category,
            name='MacBook Pro 16',
            slug='macbook-pro-16',
            price=Decimal('89999.00'),
            stock=10,
            is_available=True,
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Ноутбуки')

    def test_product_str_and_url(self):
        self.assertEqual(str(self.product), 'MacBook Pro 16')
        self.assertEqual(self.product.get_absolute_url(), reverse('shop:product_detail', args=['macbook-pro-16']))


class ShopViewAndCacheTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client()
        self.category = Category.objects.create(name='Смартфони', slug='smartphones', is_active=True)
        self.product = Product.objects.create(
            category=self.category,
            name='iPhone 15',
            slug='iphone-15',
            price=Decimal('39999.00'),
            stock=5,
            is_available=True,
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_list.html')
        self.assertContains(response, 'iPhone 15')

    def test_product_list_by_category(self):
        response = self.client.get(reverse('shop:product_list_by_category', args=['smartphones']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'iPhone 15')

    def test_product_search(self):
        response = self.client.get(reverse('shop:product_list') + '?q=iPhone')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'iPhone 15')

    def test_product_detail_view(self):
        response = self.client.get(reverse('shop:product_detail', args=['iphone-15']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_detail.html')
        self.assertContains(response, '39999')

    def test_cache_invalidation_signal(self):
        # Trigger cache populate
        self.client.get(reverse('shop:product_list'))
        self.assertIsNotNone(cache.get('shop:root_categories'))

        # Create new category to trigger post_save signal
        Category.objects.create(name='Аксесуари', slug='accessories')
        self.assertIsNone(cache.get('shop:root_categories'))
