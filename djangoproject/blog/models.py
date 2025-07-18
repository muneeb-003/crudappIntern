from django.db import models
from django.contrib.auth.models import User



class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.CharField(max_length=200)
    comment = models.TextField()
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"