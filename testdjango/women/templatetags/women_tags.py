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


@register.inclusion_tag('women/main_menu.html', takes_context=True)
def show_main_menu(context, is_auth=False):
    menu_to_display = menu if is_auth else menu[:1] + menu[2:]
    return {'menu': menu_to_display, 'is_auth': is_auth, 'request': context['request']}
