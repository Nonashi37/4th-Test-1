from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from posts.views import about, create_post, get_post, get_posts, hello, main
from users.views import login_view, logout_view, register_view, edit_profile_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", hello),
    path("", main, name="home"),
    path("about/", about),
    path("posts/", get_posts, name="post_list"),
    path("post/<int:id>/", get_post, name="post_detail"),
    path("post/create/", create_post, name="post_create"),
    path("users/register/", register_view, name="register"),
    path("users/login/", login_view, name="login"),
    path("users/logout/", logout_view, name="logout"),
    path("users/profile/edit/", edit_profile_view, name="profile_edit"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
