from django.apps import AppConfig


class ShopConfig(AppConfig):
    name = 'shop'
    verbose_name = 'Каталог товарів'

    def ready(self):
        # Підключаємо сигнали для автоматичної інвалідації кешу
        from . import signals  # noqa: F401

