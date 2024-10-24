from django.db import models


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
    image = models.ImageField(null=True, blank=True, upload_to="posts")
    title = models.CharField(max_length=70)
    content = models.TextField(null=True, blank=True)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts", blank=True, null=True)


    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.CharField(max_length=256)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
