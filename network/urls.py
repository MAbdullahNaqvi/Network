
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.allposts, name="posts"),
    path("upload", views.upload, name="upload"),
    path("accounts/<str:id>", views.accounts, name="accounts"),
    path("like",views.like, name="like"),
    path("unlike",views.unlike, name="unlike")
]
