from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="myapp/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="myapp/logout.html"),
        name="logout",
    ),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("blog/<int:blog_id>/", views.post_detail, name="post_detail"),
    path("create-blog/", views.create_blog, name="create_blog"),
    path("blog/<int:blog_id>/like/", views.like_blog, name="like_blog"),
    path("blog/<int:blog_id>/comment/", views.add_comment, name="add_comment"),
    path("edit-blog/<blog_id>/", views.edit_blog, name="edit_blog"),
    path("delete_blog/<blog_id>/", views.delete_blog, name="delete_blog"),
    path("category/<str:category>/", views.blogs_by_category, name="blogs_by_category"),
    path("blogs/", views.blog_list, name="blog_list"),
    path("contacts/", views.contacts, name="contacts"),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
