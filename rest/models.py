from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Sum

# director = 'DI'
# admin = 'AD'
# cook = 'CO'
# cashier = 'CA'
# cleaner = 'CL'
#
# POSITIONS = [
#     (director, 'Директор'),
#     (admin, 'Администратор'),
#     (cook, 'Повар'),
#     (cashier, 'Кассир'),
#     (cleaner, 'Уборщик')
# ]
#
# class Staff(models.Model):
#
#     director = 'DI'
#     admin = 'AD'
#     cook = 'CO'
#     cashier = 'CA'
#     cleaner = 'CL'
#
#     full_name = models.CharField(max_length = 255)
#     position = models.CharField(max_length=2, choices=POSITIONS, default=cashier)
#     labor_contract = models.IntegerField()
#
#     def get_last_name(self):
#         return self.full_name.split()[0]
#
# class Product(models.Model):
#     name = models.CharField(max_length = 255)
#     price = models.FloatField(default = 0.0)
#     composition = models.TextField(default="Состав не указан")
#
# class Order(models.Model):
#     time_in = models.DateTimeField(auto_now_add = True)
#     time_out = models.DateTimeField(null = True)
#     cost = models.FloatField(default = 0.0)
#     pickup = models.BooleanField(default = False)
#     complete = models.BooleanField(default = False)
#     staff = models.ForeignKey('Staff', on_delete = models.CASCADE)
#     products = models.ManyToManyField('Product', through='ProductOrder')
#
#     def finish_order(self):
#         self.time_out = datetime.now()
#         self.complete = True
#         self.save()
#
#     def get_duration(self):
#         if self.complete:
#             return (self.time_out -self.time_in).total_seconds() // 60
#         else:
#             return (datetime.now() - self.time_in).total_seconds() // 60
#
#
# class ProductOrder(models.Model):
#     product = models.ForeignKey('Product', on_delete = models.CASCADE)
#     order = models.ForeignKey('Order', on_delete = models.CASCADE)
#     _amount = models.IntegerField(default = 1, db_column = 'amount')
#
#     @property
#     def amount(self):
#         return self._amount
#
#     @amount.setter
#     def amount(self, value):
#         self._amount = int(value) if value >= 0 else 0
#         self.save()
#
#     def product_sum(self):
#         product_price = self.product.price
#         return product_price * self.amount

class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    ratings = models.IntegerField(default = 0)

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
    # def update_rating(self):
    #     postR = self.post_set.all().aggregate(postRating=Sum('rating'))
    #     p_R = 0
    #     p_R += postR.get('postRating')
    #
    #     commentR = self.authorUser.comment_set.all().aggregate(commentRating=Sum('rating'))
    #     c_R = 0
    #     c_R += commentR.get('commentRating')
    #
    #     self.ratings = p_R * 3 + c_R
    #     self.save()

class Category(models.Model):
    nameCategory = models.CharField(max_length = 255, unique = True)

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
    rating = models.IntegerField(default = 0)
    category = models.ManyToManyField(Category, through='PostCategory')
    post_author = models.ForeignKey(Author, on_delete = models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
       return f' {self.header} \n{self.text_post[0:123]}...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

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

