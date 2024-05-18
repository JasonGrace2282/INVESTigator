import django.http as http
from django.views.generic import FormView, TemplateView

from .forms import SubmitEvidenceForm
from .models import Case


class CaseView(TemplateView):
    def get_template_names(self) -> list[str]:
        base = "-caseview.html"
        return ["detective"+base] if self.request.user.is_superuser else ["witness"+base]


class SubmitEvidence(FormView):
    template_name = "submit-evidence.html"
    form_class = FormView

    def get_context_data(self, **kwargs):
        if (pk := self.request.GET.get("case")) is None:
            raise http.Http404
        context = super().get_context_data(**kwargs)
        context["case"] = Case.objects.get(pk=pk)
        return context
