from django.urls import path, include
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, PostSearch, PostCreate, PostUpdate, PostDelete, CategoryListView, subscribe
from django.views.decorators.cache import cache_page


urlpatterns = [
   path('', cache_page(5)(NewsList.as_view()), name='post_list'),
   path('<int:pk>', NewsDetail.as_view(), name='post_detail'),

   path('search/', PostSearch.as_view(), name='search'),

   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),

   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),

]

