from django.contrib import admin

from .models import Blog, FollowRelationship


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "slug", "author", "is_active")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(FollowRelationship)
class FollowRelationshipAdmin(admin.ModelAdmin):
    list_display = ("profile", "blog")
    # raw_id_fields = ('profile', 'blog')
