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
            # POCUS IQ Scale fields
            "iq_probe_choice",
            "iq_depth",
            "iq_gain_presets",
            "iq_probe_control",
            "iq_anatomy_landmarks",
            "iq_labelling",
            "iq_completeness",
            "iq_comments",
        ]
        widgets = {
            "performed_at": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 4}),
            "iq_comments": forms.Textarea(attrs={"rows": 3, "placeholder": "Optional comments on image quality..."}),
            # Radio button widgets for IQ scale
            "iq_probe_choice": forms.RadioSelect(),
            "iq_depth": forms.RadioSelect(),
            "iq_gain_presets": forms.RadioSelect(),
            "iq_probe_control": forms.RadioSelect(),
            "iq_anatomy_landmarks": forms.RadioSelect(),
            "iq_labelling": forms.RadioSelect(),
            "iq_completeness": forms.RadioSelect(),
        }
