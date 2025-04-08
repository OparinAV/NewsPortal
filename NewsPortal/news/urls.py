from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, NewsDetail


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostList.as_view()),
   path('1', NewsDetail.as_view()),
   path('2', NewsDetail.as_view()),
   path('3', NewsDetail.as_view()),
]