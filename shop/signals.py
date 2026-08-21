"""Сигнали для автоматичної інвалідації кешу при зміні товарів та категорій."""

from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Category, Product, ProductImage


def clear_shop_cache():
    """Очищення кешу категорій та списків товарів."""
    try:
        # Очищуємо специфічні ключі кешу або весь кеш
        cache.delete('shop:root_categories')
        cache.delete('shop:all_categories')
        # Якщо використовується django-redis з підтримкою delete_pattern
        if hasattr(cache, 'delete_pattern'):
            cache.delete_pattern('shop:*')
    except Exception:
        pass


@receiver([post_save, post_delete], sender=Category)
def on_category_change(sender, instance, **kwargs):
    """Інвалідація кешу при створенні, зміні або видаленні категорії."""
    clear_shop_cache()
    if instance.slug:
        cache.delete(f'shop:category:{instance.slug}')


@receiver([post_save, post_delete], sender=Product)
def on_product_change(sender, instance, **kwargs):
    """Інвалідація кешу при створенні, зміні або видаленні товару."""
    clear_shop_cache()
    if instance.slug:
        cache.delete(f'shop:product:{instance.slug}')


@receiver([post_save, post_delete], sender=ProductImage)
def on_product_image_change(sender, instance, **kwargs):
    """Інвалідація кешу товару при додаванні/видаленні фотографій."""
    clear_shop_cache()
    if instance.product and instance.product.slug:
        cache.delete(f'shop:product:{instance.product.slug}')
