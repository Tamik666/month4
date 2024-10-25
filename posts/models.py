from django.db import models
from django.contrib.auth.models import User


"""

Posts.objects.all() - All objects from db

Posts.objects.filter(title = "post) - All objects with title = post

Posts.objects.get(id = 1) - Only one object with id = 1



"""

class Tag(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):  
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", null=True)
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=70)
    content = models.TextField(null=True, blank=True)
    rate = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name="posts", null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts", null=True)
    comments = models.ManyToManyField('Comment', related_name="posts", null=True)


    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.CharField(max_length=256)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text