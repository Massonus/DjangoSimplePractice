from django.db.models import Count
from django.core.cache import cache
from .models import *


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = cache.get('categories')

        if not categories:
            categories = Category.objects.annotate(Count('women'))
            cache.set('categories', categories, 60)

        context['cats'] = categories

        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
