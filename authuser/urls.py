from django.urls import path
from django.contrib.auth import views as auth_views

from .views import register_view

app_name = "authuser"

urlpatterns = [
    path("register", register_view, name="register"),
    path(
        "login",
        auth_views.LoginView.as_view(
            template_name="authuser/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
]
