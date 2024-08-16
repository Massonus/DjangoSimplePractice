from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from .forms import *
from .utils import *


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Main page')
        # объединение двух словарей контекстов и возврат их
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        # select_related = чтобы вместе с women были загружены ещё категории для уменьшения SQL запросов
        return Women.objects.filter(is_published=True).select_related('category')


# def index(request):
#     posts = Women.objects.all()
#     context = {
#         'posts': posts,
#         'title': 'Main page',
#         'cat_selected': 0,
#     }
#
#     return render(request, 'women/index.html', context=context)

# @login_required
def about(request):
    # пример пагинации в функции представления
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'women/about.html', {'page_obj': page_obj, 'title': 'About'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/add_page.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Main page')
        return dict(list(context.items()) + list(c_def.items()))


# def add_page(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/add_page.html', {'form': form, 'title': 'Add page'})

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_user_context(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Contact')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


def categories(request, catid):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>second</h1><p>{catid}</p>")


def archive(request, year):
    if int(year) > 2024:
        return redirect('home', permanent=True)
    return HttpResponse(f'Archive for {year}')


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    # pk_url_kwarg =
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     context = {
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.category_id,
#     }
#
#     return render(request, 'women/post.html', context=context)


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True).select_related(
            'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['category_slug'])

        c_def = self.get_user_context(title=f'Category - {category.name}',
                                      cat_selected=category.pk)

        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Registration')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Login')
        return dict(list(context.items()) + list(c_def.items()))

    # def get_succesfs_url(self):
    #     return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


# def show_category(request, category_slug):
#     category_id = Category.objects.get(slug=category_slug)
#     posts = Women.objects.filter(category_id=category_id)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'title': 'Main page with categories',
#         'cat_selected': category_slug,
#     }
#
#     return render(request, 'women/index.html', context=context)


def page_note_found(request, exception):
    return HttpResponseNotFound(f'<h1>Page note found</h1>')


def practice(request):
    # from django.db import connection

    # women_list = Women.objects.all()
    # for women in women_list:
    #     print(women)
    #
    # print('-' * 30)
    # ordered_women = Women.objects.order_by('pk')

    # ordered_women = Women.objects.all().reverse() = Women.objects.all().order_by('-pk')
    # добавляем __gte (>=) или __lte (<=) к аргументу если необходимо

    # ordered_women = Women.objects.filter(time_update__gte=datetime(2024, 8, 15, 13, 7, 0))
    # for women in ordered_women:
    #     print(women)

    # print(connection.queries)

    # woman = Women.objects.get(pk=1)
    # print(woman.category.name)
    # cat = Category.objects.get(pk=1)
    # по умолчанию имя вторичной модели и добавление _set выводит все связанные объекты
    # cat.women_set.all() = cat.get_posts.all() если в Foreign Key Category добавлено related_name='get_posts'

    # print(Women.objects.filter(title__contains='ли'))
    # без учёта регистра
    # print(Women.objects.filter(title__icontains='ЛИ'))

    # __in выбирает каждое значение из итерируемого объекта
    # print(Women.objects.filter(pk__in=[1, 2, 5, 11, 12], is_published=True))
    # print(Women.objects.filter(category__in=[1, 2]))

    # cats = Category.objects.all()
    # print(Women.objects.filter(category__in=cats))

    # from django.db.models import Q

    # использование класса Q помогает строить фильтр с помощью или (|), и (&), НЕ (~) (в этом случае)
    # print(Women.objects.filter(~Q(pk__lt=5) | Q(category_id=2)))

    # выбор последнего или первого элемента из списка
    # print(Women.objects.order_by('-pk').first())
    # print(Women.objects.order_by('-pk').last())

    # print(Women.objects.latest('time_update'))
    # print(Women.objects.earliest('time_update'))

    # print(Women.objects.order_by('title').earliest('time_update'))
    # print(Women.objects.order_by('title').latest('time_update'))

    # w = Women.objects.get(pk=7)
    # формирование метода get_previous_by_ (или get_next_by_) + поле, относительно которого ищем
    # print(w.get_previous_by_time_update())
    # print(w.get_next_by_time_update())
    # print(w.get_next_by_time_update(pk__gt=10))

    # Category.objects.create(name='Sports', slug='sports')

    # c2 = Category.objects.get(pk=2)
    # c3 = Category.objects.get(pk=3)
    # # проверка есть ли хоть одна запись в рубрике
    # print(c2.women_set.exists())
    # print(c3.women_set.exists())
    # # количество записей
    # print(c2.women_set.count())
    # print(c3.women_set.count())
    # print(Women.objects.filter(pk__gt=4).count())

    # category__slug = <имя первичной модели>__<название поля первичной модели>
    # print(Women.objects.filter(category__slug='aktrisy'))
    # print(Women.objects.filter(category__in=[1]))
    # print(Women.objects.filter(category__name='Певицы'))
    # print(Women.objects.filter(category__name__contains='цы'))
    # print(Category.objects.filter(women__title__contains='ли'))
    # print(Category.objects.filter(women__title__contains='ли').distinct())

    # from django.db.models import Min, Max, Count, Sum, Avg

    # print(Women.objects.aggregate(Min('category_id'), Max('category_id')))
    # print(Women.objects.aggregate(cat_min=Min('category_id'), cat_max=Max('category_id')))
    # print(Women.objects.aggregate(res=Sum('category_id') - Count('category_id')))
    # print(Women.objects.aggregate(res=Avg('category_id')))
    # print(Women.objects.filter(pk__gt=4).aggregate(res=Avg('category_id')))

    # выбор определённого количества полей
    # print(Women.objects.values('title', 'category_id').get(pk=1))
    # print(Women.objects.values('title', 'category__name').get(pk=1))
    # w = Women.objects.values('title', 'category__name')
    # for p in w:
    #     print(p['title'], p['category__name'])

    # w = Women.objects.values('category_id').annotate(Count('id'))
    # print(w)
    # w = Women.objects.annotate(Count('id'))
    # print(w)
    # c = Category.objects.annotate(Count('women'))
    # print(c)
    # print(c[1].women__count)
    # c = Category.objects.annotate(total=Count('women'))
    # print(c[1].total)
    # c = Category.objects.annotate(total=Count('women')).filter(total__gt=0)
    # print(c)

    # from django.db.models import F
    # w = Women.objects.filter(pk__gt=F('category_id'))
    # print(w)
    # пример увеличения количества views в таблице
    # Women.objects.filter(slug='bejonse').update(views=F('views')+1)
    # w = Women.objects.get(pk=1)
    # w.views = F('views') + 1 подход более рекомендуем например при одновременном получении страницы разными юзерами
    # w.views = F('views') + 1 = m.views += 1

    # from django.db.models.functions import Length

    # ps = Women.objects.annotate(len=Length('title'))
    # for item in ps:
    #     print(item.title, item.len)

    # w = Women.objects.raw('SELECT * FROM women_women')
    # for item in w:
    #     print(item.pk, item.title)

    # from django.core.paginator import Paginator
    #
    # women = ['Angelina', 'Jennifer', 'Julia', 'Margo', 'Uma']
    # paginator = Paginator(women, 3)
    # print(paginator.count, paginator.num_pages, paginator.page_range)
    # p1 = paginator.page(1)
    # print(p1.object_list)
    # print(p1.has_next())
    # print(p1.has_previous())
    # print(p1.has_other_pages())
    # print(p1.next_page_number())
    return HttpResponse('Practice page. Look at terminal')
