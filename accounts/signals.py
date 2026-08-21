from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver

from cart.cart import merge_carts

from .models import UserProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Кожному новому користувачу автоматично створюємо профіль."""
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    """Гість поклав товари в кошик і залогінився — переносимо їх у базу та показуємо повідомлення."""
    if request:
        merge_carts(request, user=user)
        if hasattr(request, '_messages'):
            messages.success(request, f'Раді знову бачити вас, {user.username}!')


@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    """Повідомлення при виході користувача."""
    if request and hasattr(request, '_messages'):
        messages.info(request, 'Ви успішно вийшли з облікового запису.')
