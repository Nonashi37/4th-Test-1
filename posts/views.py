from django.http import HttpResponse
from django.shortcuts import render

from posts.models import Post


# Create your views here.
def hello(request):
    return HttpResponse("Hello Django!")


def main(request):

    return render(request, "base.html")


def about(request):

    return HttpResponse("<h1>About us</h1> <a href='/'>Main</a>")


def get_post(request):
    post = Post.objects.all()

    return render(request, "posts/posts_view.html", context={"posts": post})
