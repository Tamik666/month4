from django.shortcuts import redirect, render
from django.http import HttpResponse
from posts.models import Post, Comment
from posts.forms import (PostForm, PostForm2, SearchForm,CommentForm)
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import random
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


def test(request):
    return HttpResponse("Hello World")

def main_page_view(request):
    if request.method == 'GET':
        return render(request, 'base.html')
    
@login_required(login_url="/login/")
def post_list_view(request):
    limit = 3
    if request.method == 'GET':
        search = request.GET.get('search', None)
        tag = request.GET.getlist('tag', None)
        ordering = request.GET.get('ordering', None)
        page = int(request.GET.get('page', 1))
        posts = Post.objects.all()

        if search:
            posts = posts.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
                )

        if tag:
            posts = posts.filter(tags__id__in=tag)

        if ordering:
            posts = posts.order_by(ordering)

        max_pages = posts.count() / limit

        if round(max_pages) < max_pages:
            max_pages = round(max_pages) + 1
        else:
            max_pages = round(max_pages)
        
        start = (page - 1) * limit
        end = page * limit
        posts = posts[start:end]

        form = SearchForm()
        context = {
            'posts': posts,
            'form': form,
            'max_pages': range(1, max_pages + 1),
        }
        return render(
            request, 'posts/post_list.html', 
            context=context
            )

class PostListView2(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'

@login_required(login_url="/login/")
def post_detail_view(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = post.comments.all()
    
    if request.method == 'GET':
        form = CommentForm()
        return render(request, 'posts/post_detail_view.html', context={'post': post, 'form': form, 'comments': comments})  
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                text=form.cleaned_data['text'], 
                post=post, 
                user=request.user
            )
            return redirect(f"/posts/{post_id}")

        # При ошибке валидации отобразить форму с ошибками
        return render(request, 'posts/post_detail_view.html', context={'post': post, 'form': form, 'comments': comments})


@login_required(login_url="/login/")
def post_create_new(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'posts/post_create.html', context={'form': form})
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request,"post_create.html", context={"form":form})
        tags = form.cleaned_data.pop('tags')
        post = Post.objects.create(author=request.user, **form.cleaned_data)
        post.tags.set(tags)
        post.save()
        return redirect("/posts/")
    

class PostDetailView2(DetailView):
    model = Post
    template_name = 'posts/post_detail_view.html'
    context_object_name = 'post'
    lookup_url_kwarg = 'post_id'

def post_update_view(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "GET":
        form=PostForm2(instance=post)
        return render(request, 'posts/post_update.html', context={'form': form})
    if request.method == "POST":
        form = PostForm2(request.POST, request.FILES, instance=post)
        if not form.is_valid():
            return render(request, "post_create.html", context={"form": form})
        form.save()
        return redirect("/posts/")
    
def post_add_coment(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        post.rate += 1
        post.save()
        return redirect("/posts/")