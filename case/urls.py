from django.urls import path

from .views import CaseView, Dashboard, SubmitEvidence

urlpatterns = [
    path("", Dashboard.as_view(), name="dashboard"),
    path("case/<int:case_num>/", CaseView.as_view(), name="view-case"),
    path("case/<int:case_num>/evidence", SubmitEvidence.as_view(), name="add-evidence")
]
