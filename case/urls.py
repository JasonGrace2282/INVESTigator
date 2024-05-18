from django.urls import path

from .views import CaseDescription, Dashboard, SubmitEvidence

urlpatterns = [
    path("", Dashboard.as_view(), name="dashboard"),
    path("case/<int:case_num>/", CaseDescription.as_view(), name="description"),
    path("case/<int:case_num>/evidence/", SubmitEvidence.as_view(), name="add-evidence")
]
