from django.urls import path

from .views import (CaseDescription, Dashboard, EvidenceView, SubmitEvidence,
                    Test)

urlpatterns = [
    path("", Dashboard.as_view(), name="dashboard"),
    path("test", Test.as_view(), name="test"),
    path("case/<int:case_num>/", CaseDescription.as_view(), name="description"),
    path("case/<int:case_num>/evidence/", SubmitEvidence.as_view(), name="add-evidence"),
    path("case/<int:case_num>/evidence/view", EvidenceView.as_view(), name="view-evidence"),
]
