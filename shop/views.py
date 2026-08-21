"""View-функції каталогу: список товарів з фільтрами та сторінка товару з кешуванням."""

from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Product

PRODUCTS_PER_PAGE = 9
CACHE_TTL = 300  # 5 хвилин


def get_cached_root_categories():
    """Отримання списку кореневих категорій з кешу або бази даних."""
    cache_key = 'shop:root_categories'
    categories = cache.get(cache_key)
    if categories is None:
        categories = list(
            Category.objects.filter(is_active=True, parent__isnull=True).prefetch_related('children')
        )
        cache.set(cache_key, categories, CACHE_TTL)
    return categories


def product_list(request, category_slug=None):
    """Список товарів з фільтром за категорією та пошуком за назвою/описом."""
    categories = get_cached_root_categories()
    products = Product.objects.filter(is_available=True).select_related('category')

    category = None
    if category_slug:
        category_cache_key = f'shop:category:{category_slug}'
        category = cache.get(category_cache_key)
        if category is None:
            category = get_object_or_404(Category, slug=category_slug, is_active=True)
            cache.set(category_cache_key, category, CACHE_TTL)

        # Показуємо товари самої категорії та її підкатегорій.
        products = products.filter(
            Q(category=category) | Q(category__parent=category)
        )

    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    paginator = Paginator(products, PRODUCTS_PER_PAGE)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'shop/product_list.html', {
        'categories': categories,
        'category': category,
        'page': page,
        'products': page.object_list,
        'query': query,
    })


def product_detail(request, slug):
    """Детальна сторінка товару з оптимізованими зв'язками."""
    product = get_object_or_404(
        Product.objects.select_related('category').prefetch_related('images'),
        slug=slug,
        is_available=True,
    )

    related = (
        Product.objects.filter(category=product.category, is_available=True)
        .exclude(pk=product.pk)
        .select_related('category')[:4]
    )

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_products': related,
    })
