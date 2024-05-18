import django.http as http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView

from .forms import SubmitEvidenceForm
from .models import Case


class Dashboard(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login")

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cases"] = Case.objects.all()
        context["user"] = self.request.user
        return context


class CaseLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy("login")
    redirect_field_name = reverse_lazy("dashboard")

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
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        case = Case.objects.get(pk=self.kwargs["case_num"])
        case.evidences.create(**form.cleaned_data)
        return super().form_valid(form)


class Test(TemplateView):
    template_name = "log-in.html"


class EvidenceView(CaseLoginRequiredMixin, ListView):
    template_name = "evidence.html"

    def get_queryset(self):
        case = Case.objects.get(pk=self.kwargs["case_num"])
        return case.evidences.all()


    def get(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise http.Http404
        return super(EvidenceView, self).get(*args, **kwargs)
