from django.contrib.auth.models import User
from django.db import models


class Tags(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Post(models.Model):
    header = models.CharField(max_length=255)
    description = models.TextField()
    rate = models.IntegerField(null=True, blank=True)
    tags = models.ManyToManyField(Tags, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="posts", null=True, blank=True)

    def __str__(self):
        return self.header


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} → {self.post.header}"