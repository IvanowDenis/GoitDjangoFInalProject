from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from orders.models import Order
from payments.models import Transaction

User = get_user_model()


class PaymentsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='payer', password='Password123!')
        self.client.login(username='payer', password='Password123!')

        self.order = Order.objects.create(
            user=self.user,
            shipping_full_name='Остап Вишня',
            shipping_phone='+380501112233',
            shipping_country='Україна',
            shipping_city='Полтава',
            shipping_postal_code='36000',
            shipping_address_line1='вул. Гоголя, 5',
            total_amount=Decimal('500.00'),
            payment_method='card',
            status=Order.STATUS_PENDING,
        )

    def test_transaction_creation_and_str(self):
        tx = Transaction.objects.create(
            reference='TX-123456',
            order=self.order,
            amount=Decimal('500.00'),
            currency='UAH',
            user=self.user,
            status=Transaction.STATUS_SPENDING,
        )
        self.assertIn('TX-123456', str(tx))
        self.assertEqual(tx.amount, Decimal('500.00'))

    def test_initiate_payment_view(self):
        response = self.client.get(
            reverse('payments:initiate_payment', args=[self.order.order_number])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.order_number)
