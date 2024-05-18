from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView


class Dashboard(TemplateView):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return redirect(reverse("login"))
        print(self.request.user)
        return super().get(request, *args, **kwargs)

class DetectiveCase(TemplateView):
    template_name = "detective-case.html"

