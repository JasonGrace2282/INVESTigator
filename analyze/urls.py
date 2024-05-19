from django.urls import path

from .views import DataDashboard, face_prediction_view

urlpatterns = [
    path("case/<int:case_num>/evidence/view/<int:evidence_num>/", DataDashboard.as_view(), name="databoard"),
    path("process/face", face_prediction_view, name="face-analysis"),
]
