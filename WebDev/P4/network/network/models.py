from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    content = models.CharField(max_length=1024)
    datetime = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_likes", null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")

class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followings")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followers")

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments")
