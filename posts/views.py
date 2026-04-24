from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView, CreateView

from posts.forms import CommentForm, PostForm
from posts.models import Post, Tags


# ✅ stays simple, no change needed
def hello(request):
    return HttpResponse("Hello Django!")


def about(request):
    return HttpResponse("<h1>About us</h1> <a href='/'>Main</a>")


# ✅ FBV → TemplateView (just renders base.html, no logic)
class MainView(TemplateView):
    template_name = "base.html"


# ✅ FBV → ListView (tag filtering logic moved into get_queryset)
class PostListView(ListView):
    template_name = "posts/posts_view.html"
    context_object_name = "posts"

    def get_queryset(self):
        queryset = Post.objects.filter(is_published=True)\
                               .select_related("user")\
                               .order_by("-created_at")
        tag_id = self.request.GET.get("tag")
        if tag_id:
            # save selected_tag so we can reuse it in get_context_data
            self._selected_tag = get_object_or_404(Tags, pk=tag_id)
            queryset = queryset.filter(tags=self._selected_tag)
        else:
            self._selected_tag = None
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tags.objects.all()
        context["selected_tag"] = self._selected_tag
        return context


# ✅ FBV → DetailView + View (GET=show post, POST=submit comment)
class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"
    pk_url_kwarg = "id"  # your URL uses <int:id>, not <int:pk>

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments\
                                         .select_related("author")\
                                         .order_by("created_at")
        context["comment_form"] = CommentForm()
        return context

    def post(self, request, id):
        # block anonymous users
        if isinstance(request.user, AnonymousUser):
            return redirect("login")

        post = get_object_or_404(Post, pk=id)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post_detail", id=id)

        # form invalid → re-render with errors
        comments = post.comments.select_related("author").order_by("created_at")
        return self.render_to_response(self.get_context_data(
            post=post,
            comments=comments,
            comment_form=comment_form,
        ))


# ✅ FBV → CreateView (LoginRequiredMixin replaces @login_required)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/create_post.html"
    success_url = reverse_lazy("post_list")
    login_url = "/users/login/"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        form.save_m2m()  # ← ManyToMany tags, same as before
        return redirect(self.success_url)