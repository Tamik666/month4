from django.db import models


"""

Posts.objects.all() - All objects from db

Posts.objects.filter(title = "post) - All objects with title = post

Posts.objects.get(id = 1) - Only one object with id = 1



"""



class Post(models.Model):
    title = models.CharField(max_length=70)
    content = models.TextField(null=True, blank=True)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title