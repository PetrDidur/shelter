from django.conf import settings
from django.core.cache import cache

from dogs.models import Category


def get_categories_cache():
    if settings.CACHE_ENABLED:
        key = 'category_list'
        page = cache.get(key)
        if page is None:
            page = Category.objects.all()
            cache.set(key, page)
        else:
            page = Category.objects.all()

        return page
