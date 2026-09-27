from django.db import models
from django.db.models import Sum

from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # 1. Суммарный рейтинг всех статей автора * 3
        posts_sum = Post.objects.filter(author=self).aggregate(
            total=Sum('rating')
        )['total'] or 0

        # 2. Суммарный рейтинг всех комментариев, сделанных автором (user)
        comments_by_author_sum = Comment.objects.filter(user=self.user).aggregate(
            total=Sum('rating')
        )['total'] or 0

        # 3. Суммарный рейтинг всех комментариев к статьям автора
        comments_to_posts_sum = Comment.objects.filter(post__author=self).aggregate(
            total=Sum('rating')
        )['total'] or 0

        self.rating = posts_sum * 3 + comments_by_author_sum + comments_to_posts_sum
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


type_arti ='ART'
type_news ='NEW'
TYPES_POSTS =[
    (type_arti, 'Статья'),
    (type_news, 'Новости')
]

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_of_post = models.CharField(max_length=3,choices=TYPES_POSTS,default=type_news)
    time_posted = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()

    def preview(self):
        if len(self.text) > 124:
            return self.text[:124] + "..."
        return self.text

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_posted = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()


