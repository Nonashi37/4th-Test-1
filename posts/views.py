from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import CommentForm, PostForm
from posts.models import Post


def hello(request):
    return HttpResponse("Hello Django!")


def main(request):
    return render(request, "base.html")


def about(request):
    return HttpResponse("<h1>About us</h1> <a href='/'>Main</a>")


def get_posts(request):
    posts = Post.objects.filter(is_published=True).select_related("user").order_by("-created_at")
    return render(request, "posts/posts_view.html", context={"posts": posts})


def get_post(request: HttpRequest, id: int):
    post = get_object_or_404(Post, pk=id)
    comments = post.comments.select_related("author").order_by("created_at")
    comment_form = CommentForm()

    if request.method == "POST":
        if isinstance(request.user, AnonymousUser):
            return redirect("login")

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post_detail", id=id)

    return render(request, "posts/post_detail.html", context={
        "post": post,
        "comments": comments,
        "comment_form": comment_form,
    })


@login_required(login_url="/users/login/")
def create_post(request: HttpRequest):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()  # for tags ManyToMany
            return redirect("post_list")
    else:
        form = PostForm()

    return render(request, "posts/create_post.html", context={"form": form})