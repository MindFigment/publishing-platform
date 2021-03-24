from django.urls import path

from . import views


app_name = 'posts'

urlpatterns = [
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.post_detail, name='post_detail'),
    path('post/<int:post_id>/', views.PostSectionListView.as_view(),
         name='post_section_list'),
    path('post/<int:post_id>/section/<model_name>/create/',
         views.SectionCreateUpdateView.as_view(),
         name='post_section_create'),
    path('post/<int:post_id>/section/<model_name>/<id>/',
         views.SectionCreateUpdateView.as_view(),
         name='post_section_update'),
    path('section/<int:id>/delete/',
         views.SectionDeleteView.as_view(),
         name='post_section_delete'),
    path('post/<int:blog_id>/create/',
         views.create_post, name='post_create')
]
