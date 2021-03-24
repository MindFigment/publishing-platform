from django.urls import path

from . import views


app_name = 'blogs'

urlpatterns = [
    # post views
    path('', views.blog_ajax_list, name='blog_list'),
    path('new/', views.new_blog, name='new_blog'),
    path('edit/<slug:slug>', views.edit_blog, name='edit_blog'),
    path('manage/', views.manage_blogs, name='manage_blogs'),
    path('follow/', views.blog_follow, name='blog_follow'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
]
