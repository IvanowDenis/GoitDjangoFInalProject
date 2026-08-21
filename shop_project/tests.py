from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse


class RateLimitMiddlewareTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client()

    def test_rate_limit_auth_endpoints_triggers_429(self):
        # Auth rate limit is 15 requests per minute
        login_url = reverse('accounts:login')
        for _ in range(15):
            response = self.client.get(login_url)
            self.assertEqual(response.status_code, 200)

        # 16th request should be blocked with 429
        blocked_response = self.client.get(login_url)
        self.assertEqual(blocked_response.status_code, 429)
        self.assertContains(blocked_response, 'Забагато запитів', status_code=429)
