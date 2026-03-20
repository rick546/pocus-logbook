from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Scan

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Custom registration form that requires email address."""
    email = forms.EmailField(
        required=True,
        help_text="Required. Enter a valid email address.",
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email address"})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """Allows users to update their email and display name."""
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name", "class": "form-control"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name", "class": "form-control"}),
            "email": forms.EmailInput(attrs={"placeholder": "your@email.com", "class": "form-control"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("That email address is already in use by another account.")
        return email


class ScanForm(forms.ModelForm):
    class Meta:
        model = Scan
        fields = [
            "scan_context",
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
            "scan_context": forms.RadioSelect(),
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
