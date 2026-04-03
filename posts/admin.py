from django.contrib import admin

from posts.models import Post, Tags, User

admin.site.register(Post)

admin.site.register(Tags)
admin.site.register(User)
