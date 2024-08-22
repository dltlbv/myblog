from django.shortcuts import render
from .models import Blog, Comment, User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, BlogForm
from django.core.exceptions import PermissionDenied


def home(request):
    blogs = Blog.objects.top_3_most_viewed()
    return render(request, "myapp/home.html", {"object_list": blogs})


def blog_list(request):
    blogs = Blog.objects.all().order_by("-created_in")
    return render(request, "myapp/blog_list.html", {"blogs": blogs})


@login_required
def profile(request):
    user = request.user
    blog = Blog.objects.filter(author=user)
    liked_blogs = user.blog_likes.all()
    return render(
        request,
        "myapp/profile.html",
        {"user": user, "blogs": blog, "liked_blogs": liked_blogs},
    )


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "myapp/register.html", {"form": form})


def create_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect("home")
    else:
        form = BlogForm()
    return render(request, "myapp/create_blog.html", {"form": form})


def post_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.increment_views()
    return render(request, "myapp/post_detail.html", {"blog": blog})


@login_required
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
    else:
        blog.likes.add(request.user)
    return redirect("post_detail", blog_id=blog.id)


@login_required
def add_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        body = request.POST.get("body")
        if body:
            Comment.objects.create(blog=blog, author=request.user, body=body)
    return redirect("post_detail", blog_id=blog.id)


@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if blog.author != request.user:
        raise PermissionDenied("Вы не можете редактировать этот пост")

    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect("post_detail", blog_id=blog.id)
    else:
        form = BlogForm(instance=blog)

    return render(request, "myapp/edit_blog.html", {"form": form, "blog": blog})


@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if blog.author != request.user:
        raise PermissionDenied("Вы не можете удалить этот пост")

    if request.method == "POST":
        blog.delete()
        return redirect("home")

    return render(request, "myapp/delete_blog.html", {"blog": blog})


def blogs_by_category(request, category):
    blogs = Blog.objects.filter_by_category(category)
    category_display = dict(Blog.CATEGORY_CHOICES).get(
        category, "Неизвестная категория"
    )
    return render(
        request,
        "myapp/blogs_by_category.html",
        {"blogs": blogs, "category": category_display},
    )


def contacts(request):
    return render(request, "myapp/contacts.html")


def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    blogs = Blog.objects.filter(author=user).order_by("-created_in")
    return render(request, "myapp/user_profile.html", {"user": user, "blogs": blogs})
