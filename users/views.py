from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from posts.models import Post
from users.forms import RegisterForm, LoginForm
from users.models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', context={'form': form})
    
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'users/register.html', context={'form': form})
        form.cleaned_data.pop('password_confirm')
        image = form.cleaned_data.pop("image")
        age = form.cleaned_data.pop("age")
        user = User.objects.create_user(**form.cleaned_data)

        Profile.objects.create(user = user, image = image, age = age)
        return redirect('/')
    
def login_view(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'users/login.html', context={'form': form})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, 'users/login.html', context={'form': form})
        user = authenticate(**form.cleaned_data)

        if user is None:
            form.add_error(None, 'Invalid username or password')
            return render(request, 'users/login.html', context={'form': form})
        login(request, user)
        return redirect('/')
@login_required
def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('/')
    
@login_required
def profile_view(request):
    if request.method == "GET":
        posts = Post.objects.filter(author=request.user)
        return render(request, "users/profile.html", context={"posts": posts})
