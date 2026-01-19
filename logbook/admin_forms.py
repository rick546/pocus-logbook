from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Scan

User = get_user_model()

class MassAddScansForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all().order_by("username"))
    exam_type = forms.ChoiceField(choices=Scan._meta.get_field("exam_type").choices)
    count = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 21)],  # 1–20 scans
        initial=5
    )
    performed_at = forms.DateField(initial=timezone.localdate, required=False)
    prevent_duplicates_same_day = forms.BooleanField(required=False, initial=True)
