from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default = 0)

    # Обновляем рейтинг автора
    def update_rating(self):
        # 1. Рейтинг статей автора (каждая статья *3)
        post_rating = self.posts.aggregate(pr=Sum('rating'))['pr'] or 0
        post_rating *= 3

        # 2. Рейтинг комментариев автора
        comment_rating = Comment.objects.filter(user=self.user).aggregate(cr=Sum('rating'))['cr'] or 0

        # 3. Рейтинг комментариев к статьям автора
        post_comment_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Sum('rating'))['pcr'] or 0

        # Общий рейтинг
        self.rating = post_rating + comment_rating + post_comment_rating
        self.save()


class Category(models.Model):
    category = models.CharField(max_length = 255, unique = True)


class Post(models.Model):
    news = 'news'
    article = 'article'
    POSITIONS = [(news, 'Новость'), (article, 'Статья')]
    positions = models.CharField(max_length = 7,
                                choices = POSITIONS,
                                default = news)
    author = models.ForeignKey(Author, on_delete = models.CASCADE, related_name = 'posts')
    created = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField('Category', through = 'PostCategory')
    title = models.CharField(max_length = 50)
    content = models.TextField()
    rating = models.IntegerField(default = 0)

    # Метод увеличения рейтинга на 1
    def like(self):
        self.rating += 1
        self.save()

    # Метод уменьшения рейтинга на 1
    def dislike(self):
        self.rating -= 1
        self.save()

    # предварительный просмотр статьи длиной 124 символа
    def preview(self):
        return f'{self.content[:124]}:'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default = 0)

    # Метод увеличения рейтинга на 1
    def like(self):
        self.rating += 1
        self.save()

    # Метод уменьшения рейтинга на 1
    def dislike(self):
        self.rating -= 1
        self.save()
