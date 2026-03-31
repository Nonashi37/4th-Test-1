from django.db import models

# Create your models here.

# INSERT INTO posts_post () ==> Post.objects.create(header="dasda", description="tesdad", user=1, rate=1)

# SELECT * FROM posts_post; ==> posts = Post.objects.all()

# SELECT * FROM posts_post WHERE user = 1; ==> posts = Post.objects.filter(user=1)

# UPDATE FROM posts_post SET user = 2 WHERE user = 1; post = posts[1]
# post.user = 2


# SELECT * FROM posts_post WHERE id = 1; post = Posts.objects.get(id=1)


# SELECT * FROM posts_post WHERE header ILIKE '% AB %'; posts = Post.objects.filter(header__icontains="ab", is_deleted = False)
class Post(models.Model):
    header = models.CharField(max_length=255)
    description = models.TextField()
    user = models.IntegerField(null=True, blank=True)
    rate = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.header} -- {self.user}"
