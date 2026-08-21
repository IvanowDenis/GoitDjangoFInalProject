from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from orders.forms import OrderCheckoutForm, ShippingAddressForm
from orders.models import Order, OrderItem, ShippingAddress
from shop.models import Category, Product

User = get_user_model()


class OrdersTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='buyer', password='Password123!')
        self.client.login(username='buyer', password='Password123!')

        self.category = Category.objects.create(name='Кава', slug='coffee')
        self.product = Product.objects.create(
            category=self.category,
            name='Арабіка 1кг',
            slug='arabica-1kg',
            price=Decimal('600.00'),
            stock=15,
            is_available=True,
        )

        self.address = ShippingAddress.objects.create(
            user=self.user,
            full_name='Іван Франко',
            phone='+380671112233',
            country='Україна',
            city='Львів',
            postal_code='79000',
            address_line1='вул. Шевченка, 10',
            is_default=True,
        )

    def test_shipping_address_form(self):
        form = ShippingAddressForm(data={
            'full_name': 'Тарас Шевченко',
            'phone': '+380679998877',
            'country': 'Україна',
            'city': 'Київ',
            'postal_code': '01001',
            'address_line1': 'вул. Хрещатик, 24',
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_order_creation_flow(self):
        # 1. Add item to cart
        self.client.post(
            reverse('cart:cart_add', args=[self.product.id]),
            {'quantity': 2, 'override': False},
        )

        # 2. Select address
        session = self.client.session
        session['shipping_address_id'] = self.address.id
        session.save()

        # 3. Confirm checkout with agree_terms=True
        response = self.client.post(
            reverse('orders:checkout_confirm'),
            {
                'payment_method': 'cash',
                'notes': 'Швидка доставка',
                'agree_terms': 'on',
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        # 4. Verify order created in DB
        order = Order.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.total_amount, Decimal('1200.00'))
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.get_total_items(), 2)

        # 5. Verify stock decreased
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 13)
