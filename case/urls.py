from django.urls import include, path

from .views import CaseDescription, Dashboard, EvidenceView, SubmitEvidence

urlpatterns = [
    path("", Dashboard.as_view(), name="dashboard"),
    path("case/<int:case_num>/", CaseDescription.as_view(), name="description"),
    path("case/<int:case_num>/evidence/", SubmitEvidence.as_view(), name="add-evidence"),
    path("", include("analyze.urls")),
    path("case/<int:case_num>/evidence/view", EvidenceView.as_view(), name="view-evidence"),
]
