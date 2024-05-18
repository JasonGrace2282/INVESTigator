from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class Login(auth_views.LoginView):
    template_name = "log-in.html"
    next_page = reverse_lazy("dashboard")

    def post(self, *args, **kwargs):
        print(self.request.POST)
        return super().post(*args, **kwargs)


class ResetPassword(auth_views.PasswordResetView):
    template_name = "reset-password.html"
