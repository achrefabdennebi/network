
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # API Routes
    path("save", views.createPost, name="createPost"),
    path("update", views.updatePost, name="updatePost"),
    path("posts", views.getPostList, name="posts"),
    path("profile/<int:profile_id>", views.getProfile, name="profile"),
    path("following", views.following, name="following")
]
