from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, reverse
from django.views.generic import FormView, TemplateView

from .forms import SubmitEvidenceForm
from .models import Case


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cases"] = Case.objects.all()
        context["user"] = self.request.user
        return context


class CaseLoginRequiredMixin(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["case"] = Case.objects.get(pk=self.kwargs["case_num"])
        context["user"] = self.request.user
        return context


class CaseDescription(CaseLoginRequiredMixin, TemplateView):
    template_name = "description.html"


class SubmitEvidence(CaseLoginRequiredMixin, FormView):
    template_name = "submit-evidence.html"
    form_class = SubmitEvidenceForm
