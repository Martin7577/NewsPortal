from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment, MyModel
from modeltranslation.admin import TranslationAdmin


# class CategoryAdmin(TranslationAdmin):
#     model = Category


class MyModelAdmin(TranslationAdmin):
    model = MyModel


# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('header', 'text_post') # генерируем список имён всех полей для более красивого отображения
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'ratings')

class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.get_fields()]

class PostCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PostCategory._meta.get_fields()]


admin.site.register(MyModel)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
