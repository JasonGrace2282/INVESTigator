from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView

from .faceprediction import prediction
from .license import read_frame
from .models import Case


class DataDashboard(TemplateView):
    template_name = "data-dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        case = Case.objects.get(pk=self.kwargs["case_num"])
        evidence = case.evidences.get(pk=self.kwargs["evidence_num"])

        context["case"] = case
        context["evidence"] = evidence

        if (vpath := settings.MEDIA_ROOT / evidence.video.name).exists():
            context["videopath"] = vpath
        if (ipath := settings.MEDIA_ROOT / evidence.image.name).exists():
            context["imagepath"] = ipath
        return context


def face_prediction_view(request) -> JsonResponse:
    path = request.GET["path"]
    return JsonResponse({
        "emotion": prediction(path)
    })

def read_licenses(request) -> JsonResponse:
    path = request.GET["path"]
    timestamps, plates, pvalues = sorted(
        zip(*read_frame(path)),
        key=lambda *_, p: p,  # type: ignore
        reversed=True
    )
    return JsonResponse({
        "timestamps": timestamps,
        "plates": plates,
        "pvalues": pvalues,
    })
