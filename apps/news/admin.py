from django.contrib import admin
from .models import News, Tag, NewsTag


class NewsTagInline(admin.TabularInline):
    model = NewsTag
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'subcategory', 'published_at', 'is_urgent')
    list_filter = ('category', 'subcategory', 'is_urgent')
    search_fields = ('title', 'content')
    inlines = [NewsTagInline]
    prepopulated_fields = {}

