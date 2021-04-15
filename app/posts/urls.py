from django.urls import path

from . import api, views

app_name = "posts"

urlpatterns = [
    path(
        "<int:year>/<int:month>/<int:day>/<slug:slug>/",
        views.post_detail,
        name="post_detail",
    ),
    path("post/<int:blog_id>/create/", views.create_post, name="create_post"),
    path("post/<slug:post_slug>/edit/", views.edit_post, name="edit_post"),
    path("delete/<int:post_id>", views.delete_post, name="delete_post"),
    path("manage/<slug:blog_slug>", views.manage_posts, name="manage_posts"),
    path("", views.post_list, name="post_list"),
    path("detailed/", api.get_detailed_posts, name="post_detailed"),
]
