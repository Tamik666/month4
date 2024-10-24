from django.contrib import admin
from posts.models import Post,Comment,Tag,Category

admin.site.register(Post)

admin.site.register(Comment)

admin.site.register(Tag)

admin.site.register(Category)