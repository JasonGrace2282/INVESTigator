from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class Login(auth_views.LoginView):
    template_name = "login.html"
    next_page = reverse_lazy("dashboard")


class ResetPassword(auth_views.PasswordResetView):
    template_name = "reset-password.html"
