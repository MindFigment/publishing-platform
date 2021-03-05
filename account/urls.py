from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('login/', views.user_login, name='login'),
    path('profiles/<username>/', views.profile_detail, name='profile_detail'),
    # path('ajax/login', views.ajax_login, name='ajax_login')
]
