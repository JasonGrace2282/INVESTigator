from django.urls import path

from .views import DataDashboard

urlpatterns = [
    path("case/<int:case_num>/evidence/view/<int:evidence_num>/", DataDashboard.as_view(), name="databoard")
]
