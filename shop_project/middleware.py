"""Middleware для обмеження частоти запитів (Rate Limiting) та захисту від DDoS / брутфорсу."""

import time
from django.core.cache import cache
from django.http import HttpResponse


class RateLimitMiddleware:
    """
    Простий та ефективний Rate Limiter на основі кешу (Redis / LocMem).
    Обмежує кількість запитів з однієї IP-адреси за заданий інтервал часу.
    """

    # Ліміти: кількість запитів / вікно в секундах
    DEFAULT_RATE = 120  # 120 запитів на хвилину для загальних сторінок
    AUTH_RATE = 15     # 15 запитів на хвилину для авторизації/реєстрації
    WINDOW_SECONDS = 60

    AUTH_PATHS = ('/accounts/login/', '/accounts/signup/', '/payments/process/')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)
        path = request.path

        # Визначаємо ліміт залежно від шляху
        limit = self.AUTH_RATE if any(path.startswith(p) for p in self.AUTH_PATHS) else self.DEFAULT_RATE
        cache_key = f"ratelimit:{ip}:{path if limit == self.AUTH_RATE else 'general'}"

        try:
            current_requests = cache.get(cache_key, 0)
            if current_requests >= limit:
                return HttpResponse(
                    "<h1>429 Too Many Requests</h1><p>Забагато запитів. Будь ласка, зачекайте хвилину перед повторною спробою.</p>",
                    status=429,
                    content_type="text/html; charset=utf-8",
                )
            # Збільшуємо лічильник
            if current_requests == 0:
                cache.set(cache_key, 1, timeout=self.WINDOW_SECONDS)
            else:
                cache.incr(cache_key)
        except Exception:
            # Якщо кеш тимчасово недоступний, пропускаємо запит
            pass

        return self.get_response(request)

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '127.0.0.1')
