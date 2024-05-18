from django.urls import path

from .views import Login, ResetPassword

urlpatterns = [
    path("", Login.as_view(), name="login"),
    path("reset", ResetPassword.as_view(), name="password_reset")
]
