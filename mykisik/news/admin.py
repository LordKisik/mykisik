from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Comment, News, Category


class NewsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "created_at",
        "updated_at",
        "get_html_photo",
        "is_published",
        "category",
    )
    list_display_links = ("id", "title")
    search_fields = ("title", "content")
    list_editable = ("is_published",)
    list_filter = ("is_published", "category")
    fields = (
        "title",
        "content",
        "photo",
        "get_html_photo",
        "is_published",
        "category",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("created_at", "updated_at", "get_html_photo")
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Фото"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "news", "text", "created")


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)

admin.site.site_title = "Админ-панель сайта помощи животным"
admin.site.site_header = "Админ-панель сайта помощи животным"
