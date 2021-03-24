from django.contrib import admin

from .models import Post, Section
from common.image import get_image_preview, get_edit_link


class SectionInline(admin.StackedInline):
    model = Section
    # fields = ['content_type', 'object_id', get_edit_link]
    # readonly_fields = [get_edit_link]
    fields = ['content_type', 'object_id']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # list_display = ('blog', 'publish',
    #                 'status', get_image_preview)
    # readonly_fields = [get_image_preview]
    list_display = ('blog', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'blog')
    # search_fields = ('title', 'body')
    # prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('blog',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    inlines = [SectionInline]
