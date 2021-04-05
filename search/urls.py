from django.urls import path

from . import views
from . import api


app_name = 'search'

urlpatterns = [
    path('', views.search, name='search'),
    path('posts/similar/',
         api.get_most_similar_posts,
         name='most_similar_posts'),
]
