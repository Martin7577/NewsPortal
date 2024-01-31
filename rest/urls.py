from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, PostSearch, PostCreate, PostUpdate, PostDelete


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем новостям у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', NewsList.as_view(), name='post_list'),
   path('<int:pk>', NewsDetail.as_view(), name='post_detail'),
   path('search/', PostSearch.as_view(), name='search'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),
]

