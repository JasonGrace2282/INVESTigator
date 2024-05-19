from django.urls import path

from .views import (DataDashboard, audio_processing, face_prediction_view,
                    read_licenses)

urlpatterns = [
    path("case/<int:case_num>/evidence/view/<int:evidence_num>/", DataDashboard.as_view(), name="databoard"),
    path("process/face", face_prediction_view, name="face-analysis"),
    path("process/license", read_licenses, name="license-finder"),
    path("process/audio", audio_processing, name="audio-sentiment"),
]
