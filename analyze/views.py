from pathlib import Path

from django.http import JsonResponse
from django.views.generic import TemplateView

from .faceprediction import prediction
from .license import read_frame
from .models import Case


class DataDashboard(TemplateView):
    template_name = "databoard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        case = Case.objects.get(pk=self.kwargs["case_num"])
        evidence = case.evidences.get(pk=self.kwargs["evidence_num"])

        context["case"] = case
        context["evidence"] = evidence

        if Path(evidence.video.path).exists():
            context["videopath"] = evidence.video.path
        if Path(evidence.image.path).exists():
            context["facepath"] = evidence.image.path
        return context


def face_prediction_view(request, path: str) -> JsonResponse:
    return JsonResponse({
        "emotion": prediction(path)
    })
