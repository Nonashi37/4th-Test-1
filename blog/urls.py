from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from posts.views import (
    PostCreateView, PostDetailView,
    PostListView, MainView,
    hello, about,
)
from users.views import (
    LoginView, LogoutView,
    RegisterView, EditProfileView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", hello),                                              # kept as FBV (no template, no logic)
    path("", MainView.as_view(), name="home"),
    path("about/", about),                                              # kept as FBV (same reason)
    path("posts/", PostListView.as_view(), name="post_list"),
    path("post/<int:id>/", PostDetailView.as_view(), name="post_detail"),
    path("post/create/", PostCreateView.as_view(), name="post_create"),
    path("users/register/", RegisterView.as_view(), name="register"),
    path("users/login/", LoginView.as_view(), name="login"),
    path("users/logout/", LogoutView.as_view(), name="logout"),
    path("users/profile/edit/", EditProfileView.as_view(), name="profile_edit"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)