from django.contrib import admin
from posts.models import Comment, Post, Tags


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("header", "user", "is_published", "created_at")
    list_filter = ("is_published",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_at")


admin.site.register(Tags)