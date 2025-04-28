from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post, Author


# Создаем свой набор фильтров для модели News.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.


class PostFilter(FilterSet):
   creationDate = DateTimeFilter(
        field_name='created',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

   class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по заголовку
           'title': ['icontains'],
           # поиск по автору
           'author': ['in'],
       }