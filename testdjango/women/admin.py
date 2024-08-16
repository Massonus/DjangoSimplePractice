from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


class WomenAdmin(admin.ModelAdmin):
    # список полей, которые хотим видеть в админке
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')
    # поля со ссылками, чтобы можно было из админки перейти на соответсвующую страницу
    list_display_links = ('id', 'title')
    # по каким полям можно производить поиск инфы
    search_fields = ('title', 'content')
    # список полей, которые можно редактировать прямо в таблице админке
    list_editable = ('is_published',)
    # поля, по которым можно фильтровать список в админке
    list_filter = ('is_published', 'time_create')
    # заполнение поля слага (в этом случае на основе имени)
    prepopulated_fields = {"slug": ("title",)}
    fields = (
    'title', 'slug', 'category', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f'<img src="{object.photo.url}" width=50>')

    get_html_photo.short_description = 'min'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    # заполнение поля слага (в этом случае на основе имени)
    prepopulated_fields = {"slug": ("name",)}


# регистрация классов в админке
admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Women admin panel'
admin.site.site_header = 'Women admin panel'
