from django import forms
from .models import Scan


class ScanForm(forms.ModelForm):
    class Meta:
        model = Scan
        fields = [
            "performed_at",
            "exam_type",
            "indication",
            "finding",
            "confidence",
            "supervisor_present",
            "supervisor_name",
            "notes",
        ]
        widgets = {
            "performed_at": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }
