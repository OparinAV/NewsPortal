# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from gc import get_objects

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from pyexpat.errors import messages
from unicodedata import category

from .models import Author, Category, Post, PostCategory, Comment, Subscription
from .filters import PostFilter
from .forms import NewsForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, get_object_or_404, render




class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    # указываем количество записей на странице
    paginate_by = 10

    # Переопределяем функцию получения списка новостей
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'created'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news_detail.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news_detail'

# Добавляем новое представление для создания товаров.
class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.change_post'
    # Указываем нашу разработанную форму
    form_class = NewsForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_edit.html'


    def form_valid(self, form):
        post = form.save(commit=False)

        # Определяем тип поста на основе URL
        if self.request.path == "/news/articles/create/":
            post.positions = 'article'
        else:
            post.positions = 'news'
        post.save()
        return super().form_valid(form)

class PostEdit(UpdateView, PermissionRequiredMixin, LoginRequiredMixin):
    permission_required = 'news.change_post'
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs["pk"])
        queryset = Post.objects.filter(category=self.category).order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    # message = 'Вы успешно подписались на рассылку новостей категории'
    return redirect("category_list", pk)

@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    return redirect("category_list", pk)