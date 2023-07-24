from django.contrib import admin
from .models import Post, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_at", "update_at", "category", "is_publish"]
    list_display_links = ["title"]
    list_editable = ["is_publish"]
    search_fields = ["title", "category"]
    list_filter = ["is_publish"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title"]
    list_display_links = ["title"]
    search_fields = ["title"]
