import django.http as http
from django.shortcuts import redirect, reverse
from django.views.generic import FormView, TemplateView

from .forms import SubmitEvidenceForm
from .models import Case


class Dashboard(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cases"] = Case.objects.all()
        context["user"] = self.request.user
        return context

    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return redirect(reverse("login"))
        return super().get(request, *args, **kwargs)


class CaseView(TemplateView):
    def get_template_names(self) -> list[str]:
        base = "-caseview.html"
        return ["detective"+base] if self.request.user.is_superuser else ["witness"+base]

    def get_context_data(self, case_num: int, **kwargs):
        context = super().get_context_data(**kwargs)
        context["case"] = Case.objects.get(pk=case_num)


class SubmitEvidence(FormView):
    template_name = "submit-evidence.html"
    form_class = SubmitEvidenceForm

    def get_context_data(self, **kwargs):
        if (pk := self.request.GET.get("case")) is None:
            raise http.Http404
        context = super().get_context_data(**kwargs)
        context["case"] = Case.objects.get(pk=pk)
        return context
