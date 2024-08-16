import os
from datetime import datetime

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def get_image_filename(instance, filename):
    ext = filename.split('.')[-1]
    title_slug = slugify(instance.slug)
    filename = f'{title_slug}.{ext}'
    return os.path.join('photos', datetime.now().strftime('%Y/%m/%d'), filename)


class Women(models.Model):
    # verbose_name для отображения соответсвующего поля в админке
    title = models.CharField(max_length=255, verbose_name='title')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to=get_image_filename)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # для отображения в админке
    class Meta:
        verbose_name = 'Famous women'
        verbose_name_plural = 'Famous women'
        ordering = ['time_create', 'title']


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True,
                            verbose_name='Category')  # поле индексировано, то есть поиск по нему будет быстрее
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    # для отображения в админке
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id']
