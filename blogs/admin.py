from django.contrib import admin

from .models import Blog, Post


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'blog', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'blog')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('blog',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
