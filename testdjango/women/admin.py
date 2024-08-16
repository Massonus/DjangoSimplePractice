from django.contrib import admin
from .models import *


class WomenAdmin(admin.ModelAdmin):
    # список полей, которые хотим видеть в админке
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
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


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    # заполнение поля слага (в этом случае на основе имени)
    prepopulated_fields = {"slug": ("name",)}


# регистрация классов в админке
admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)
