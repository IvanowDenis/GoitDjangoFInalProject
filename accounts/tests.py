from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from accounts.forms import SignUpForm, UserProfileForm
from accounts.models import UserProfile

User = get_user_model()


class AccountsModelAndSignalTests(TestCase):
    def test_user_profile_created_on_user_creation_signal(self):
        user = User.objects.create_user(username='testuser', password='password123')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
        profile = user.profile
        self.assertEqual(str(profile), 'Профіль testuser')


class AccountsFormTests(TestCase):
    def test_signup_form_valid(self):
        form = SignUpForm(data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPass123!#',
            'password2': 'StrongPass123!#',
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_signup_form_passwords_mismatch(self):
        form = SignUpForm(data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPass123!#',
            'password2': 'DifferentPass123!#',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_user_profile_form(self):
        form = UserProfileForm(data={
            'phone': '+380501234567',
            'date_of_birth': '1995-05-15',
        })
        self.assertTrue(form.is_valid(), form.errors)


class AccountsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='john', password='Password123!')

    def test_signup_view_get(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_signup_view_post_success(self):
        response = self.client.post(reverse('accounts:signup'), {
            'username': 'bob',
            'email': 'bob@example.com',
            'password1': 'Password123!#',
            'password2': 'Password123!#',
        })
        self.assertRedirects(response, reverse('shop:product_list'))
        self.assertTrue(User.objects.filter(username='bob').exists())

    def test_profile_view_requires_login(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_view_logged_in(self):
        self.client.login(username='john', password='Password123!')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
