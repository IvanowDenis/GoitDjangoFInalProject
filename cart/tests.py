from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from cart.models import Cart, CartItem
from shop.models import Category, Product

User = get_user_model()


class CartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Книги', slug='books')
        self.product = Product.objects.create(
            category=self.category,
            name='Python Crash Course',
            slug='python-crash-course',
            price=Decimal('1000.00'),
            stock=10,
            is_available=True,
        )

    def test_session_cart_workflow(self):
        # 1. Add product
        response = self.client.post(
            reverse('cart:cart_add', args=[self.product.id]),
            {'quantity': 2},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        # 2. View cart detail
        detail_response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, 'Python Crash Course')

        # 3. Update quantity
        update_response = self.client.post(
            reverse('cart:cart_update', args=[self.product.id]),
            {'quantity': 3},
            follow=True,
        )
        self.assertEqual(update_response.status_code, 200)

        # 4. Remove product
        remove_response = self.client.post(
            reverse('cart:cart_remove', args=[self.product.id]),
            follow=True,
        )
        self.assertEqual(remove_response.status_code, 200)
        self.assertContains(remove_response, 'Ваш кошик порожній')

    def test_database_cart_for_authenticated_user(self):
        user = User.objects.create_user(username='tester', password='Password123!')
        self.client.login(username='tester', password='Password123!')

        self.client.post(
            reverse('cart:cart_add', args=[self.product.id]),
            {'quantity': 3},
        )

        db_cart = Cart.objects.get(user=user, paid_status=False)
        self.assertEqual(db_cart.get_total_items(), 3)
        self.assertEqual(db_cart.get_total_price(), Decimal('3000.00'))
