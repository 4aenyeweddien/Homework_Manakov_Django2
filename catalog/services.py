from django.core.cache import cache

from .models import Product, Category
from config.settings import CACHE_ENABLED


def get_products_by_category(category_id):
    """Возвращает все продукты в указанной категории"""
    return Product.objects.filter(category_id=category_id)


def get_category(category_id):
    """Получение категории по ID"""
    from django.shortcuts import get_object_or_404
    return get_object_or_404(Category, id=category_id)


def get_products_from_cache():
    """Получает данные по продуктам из кэша, если кэш пуст, получает данные из БД"""

    if not CACHE_ENABLED:
        return Product.objects.all()
    key = "products_list"
    cache.get(key)
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products