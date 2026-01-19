from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count
from django.urls import path
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Scan
from .admin_forms import MassAddScansForm

from django.contrib import admin
from .models import ClinicalCase, CaseStep, CaseQuestion, CaseChoice

admin.site.register(ClinicalCase)
admin.site.register(CaseStep)
admin.site.register(CaseQuestion)
admin.site.register(CaseChoice)

User = get_user_model()


@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "exam_type", "performed_at")
    list_filter = ("exam_type", "performed_at", "user")
    search_fields = ("user__username",)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("mass-add/", self.admin_site.admin_view(self.mass_add_view), name="scan_mass_add"),
        ]
        return custom_urls + urls

    def mass_add_view(self, request):
        if request.method == "POST":
            form = MassAddScansForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data["user"]
                exam_type = form.cleaned_data["exam_type"]
                count = int(form.cleaned_data["count"])
                performed_at = form.cleaned_data["performed_at"] or timezone.localdate()
                prevent_dup = form.cleaned_data["prevent_duplicates_same_day"]

                created = 0
                skipped = 0

                for _ in range(count):
                    if prevent_dup:
                        obj, was_created = Scan.objects.get_or_create(
                            user=user,
                            exam_type=exam_type,
                            performed_at=performed_at,
                        )
                        if was_created:
                            created += 1
                        else:
                            skipped += 1
                            # If you’re preventing duplicates and one already exists for the day,
                            # creating more would keep skipping—so break.
                            break
                    else:
                        Scan.objects.create(
                            user=user,
                            exam_type=exam_type,
                            performed_at=performed_at,
                        )
                        created += 1

                if skipped:
                    messages.warning(request, f"Created {created} scan(s). Skipped {skipped} due to duplicate prevention.")
                else:
                    messages.success(request, f"Created {created} scan(s) for {user.username}.")

                return redirect("..")
        else:
            form = MassAddScansForm()

        context = {
            **self.admin_site.each_context(request),
            "title": "Mass add scans",
            "form": form,
        }
        return render(request, "admin/logbook/scan/mass_add.html", context)

