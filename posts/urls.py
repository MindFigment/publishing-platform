from django.urls import path

from . import views
from . import api


app_name = 'posts'

urlpatterns = [
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.post_detail, name='post_detail'),
    path('post/<int:blog_id>/create/',
         views.create_post, name='post_create'),
    path('manage/<slug:blog_slug>',
         views.manage_posts,
         name='manage_posts'),
    path('delete/<int:post_id>', views.delete_post, name='delete_post'),
    path('', views.post_list, name='post_list'),
    path('detailed/', api.get_detailed_posts, name='post_detailed'),
]
