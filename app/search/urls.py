from django.urls import path

from . import views
from . import api


app_name = 'search'

urlpatterns = [
    path('', views.search_blogs_and_posts, name='search_blogs_and_posts'),
    path('posts/similar',
         api.get_most_similar_posts,
         name='most_similar_posts'),
]
