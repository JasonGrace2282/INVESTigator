from django import forms

from .models import Evidence


class SubmitEvidenceForm(forms.ModelForm):
    class Meta:
        model = Evidence
        fields = ["email", "text", "image", "video", "audio"]
