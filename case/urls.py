from django.urls import path

from .views import CaseView, Dashboard, SubmitEvidence

urlpatterns = [
    path("", Dashboard.as_view(), name="dashboard"),
    path("case/<int:case_num>/", CaseView, name="view-case"),
    path("case/<int:case_num>/evidence", SubmitEvidence, name="add-evidence")
]
