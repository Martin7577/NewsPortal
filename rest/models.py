from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.cache import cache




class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    ratings = models.IntegerField(default = 0)

    def __str__(self):
        return self.user.username

    def update_ratings(self):
        post_rating = 0
        comment_rating = 0
        post_comment_rating = 0

        posts = Post.objects.filter(post_author=self)
        for p in posts:
            post_rating += p.rating
        comments = Comment.objects.filter(user=self.user)
        for c in comments:
            comment_rating += (c.rating)
        post_comment = Comment.objects.filter(post__post_author=self)
        for pc in post_comment:
            post_comment_rating += pc.rating

        print(post_rating)
        print('------------')
        print(comment_rating)
        print('------------')
        print(post_comment_rating)


        self.ratings = post_rating * 3 + comment_rating + post_comment_rating
        self.save()


class Category(models.Model):
    nameCategory = models.CharField(max_length = 255, unique = True)
    subscribers = models.ManyToManyField(User, related_name="categories")

    def __str__(self):
        return self.nameCategory

class Post(models.Model):
    article = 'AR'
    news = 'NW'
    CATEGORIES = [
        (article, 'Статья'),
        (news, 'Новость')
    ]
    article_or_news = models.CharField(max_length=2, choices=CATEGORIES, default=news)
    time_in = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=255)
    text_post = models.TextField()
    rating = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through='PostCategory')
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}')

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
       return f' {self.header} \n{self.text_post[0:123]}...'

    def __str__(self):
        return self.header

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.header} {self.category.nameCategory}'

class Comment(models.Model):
    text_comment = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default = 0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

