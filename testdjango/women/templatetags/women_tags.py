from django import template
from ..models import *

register = template.Library()

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': 'Практика', 'url_name': 'pract'},
        ]


@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('women/main_menu.html')
def show_main_menu(is_auth=False):
    if not is_auth:
        un_auth_menu = menu.copy()
        un_auth_menu.pop(1)
        return {'menu': un_auth_menu}
    return {'menu': menu}
