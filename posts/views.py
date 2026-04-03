from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from posts.models import Post


# Create your views here.
def hello(request):
    return HttpResponse("Hello Django!")


def main(request):

    return render(request, "base.html")


def about(request):

    return HttpResponse("<h1>About us</h1> <a href='/'>Main</a>")


def get_posts(request):
    post = Post.objects.all()

    return render(request, "posts/posts_view.html", context={"posts": post})


def get_post(request, id):
    post = get_object_or_404(Post, pk=id)
    return render(request, "posts/post_detail.html", context={"post": post})
