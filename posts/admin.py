from django.contrib import admin

from .models import Post, Section


class SectionInline(admin.StackedInline):
    model = Section
    fields = ['content_type', 'object_id']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('blog', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'blog')
    raw_id_fields = ('blog',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    inlines = [SectionInline]
