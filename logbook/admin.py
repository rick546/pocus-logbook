import csv
from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count, Q
from django.urls import path
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse

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
    list_display = ("id", "user", "exam_type", "scan_context", "performed_at")
    list_filter = ("exam_type", "scan_context", "performed_at", "user")
    search_fields = ("user__username",)
    actions = ["export_user_scan_summary", "export_detailed_scans"]

    def export_user_scan_summary(self, request, queryset):
        """Export a summary of all users' scans to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_scan_summary.csv"'

        writer = csv.writer(response)

        # Header row
        header = [
            'Username', 'Email', 'Total Scans',
            'Academic Half Day', 'Self Logged',
            'RUQ', 'LUQ', 'Aorta', 'Subxiphoid',
            'PLAX', 'PSAX', 'IVC', 'OB First Trimester'
        ]
        writer.writerow(header)

        # Get all users who have scans
        users_with_scans = User.objects.filter(scans__isnull=False).distinct()

        for user in users_with_scans:
            user_scans = Scan.objects.filter(user=user)

            row = [
                user.username,
                user.email,
                user_scans.count(),
                user_scans.filter(scan_context='ACADEMIC').count(),
                user_scans.filter(scan_context='SELF').count(),
                user_scans.filter(exam_type='RUQ').count(),
                user_scans.filter(exam_type='LUQ').count(),
                user_scans.filter(exam_type='AORTA').count(),
                user_scans.filter(exam_type='SUBXIPHOID').count(),
                user_scans.filter(exam_type='PLAX').count(),
                user_scans.filter(exam_type='PSAX').count(),
                user_scans.filter(exam_type='IVC').count(),
                user_scans.filter(exam_type='OB_FIRST').count(),
            ]
            writer.writerow(row)

        self.message_user(request, f"Exported scan summary for {users_with_scans.count()} users.")
        return response

    export_user_scan_summary.short_description = "Export User Scan Summary (CSV)"

    def export_detailed_scans(self, request, queryset):
        """Export detailed scan records to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="detailed_scans.csv"'

        writer = csv.writer(response)

        # Header row
        header = [
            'ID', 'Username', 'Email', 'Exam Type', 'Scan Context',
            'Performed At', 'Finding', 'Indication', 'Supervisor Present',
            'Supervisor Name', 'Confidence', 'Notes', 'Created At'
        ]
        writer.writerow(header)

        # Export selected scans or all if none selected
        scans = queryset if queryset.exists() else Scan.objects.all()

        for scan in scans.select_related('user'):
            row = [
                scan.id,
                scan.user.username,
                scan.user.email,
                scan.get_exam_type_display(),
                scan.get_scan_context_display(),
                scan.performed_at,
                scan.get_finding_display(),
                scan.indication,
                'Yes' if scan.supervisor_present else 'No',
                scan.supervisor_name,
                scan.confidence or '',
                scan.notes,
                scan.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            ]
            writer.writerow(row)

        self.message_user(request, f"Exported {scans.count()} scan records.")
        return response

    export_detailed_scans.short_description = "Export Detailed Scans (CSV)"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("mass-add/", self.admin_site.admin_view(self.mass_add_view), name="scan_mass_add"),
            path("export-summary/", self.admin_site.admin_view(self.export_summary_view), name="scan_export_summary"),
            path("export-all/", self.admin_site.admin_view(self.export_all_view), name="scan_export_all"),
        ]
        return custom_urls + urls

    def export_summary_view(self, request):
        """Export all users' scan summary directly"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_scan_summary.csv"'

        writer = csv.writer(response)

        header = [
            'Username', 'Email', 'Total Scans',
            'Academic Half Day', 'Self Logged',
            'RUQ', 'LUQ', 'Aorta', 'Subxiphoid',
            'PLAX', 'PSAX', 'IVC', 'OB First Trimester'
        ]
        writer.writerow(header)

        users_with_scans = User.objects.filter(scans__isnull=False).distinct()

        for user in users_with_scans:
            user_scans = Scan.objects.filter(user=user)
            row = [
                user.username,
                user.email,
                user_scans.count(),
                user_scans.filter(scan_context='ACADEMIC').count(),
                user_scans.filter(scan_context='SELF').count(),
                user_scans.filter(exam_type='RUQ').count(),
                user_scans.filter(exam_type='LUQ').count(),
                user_scans.filter(exam_type='AORTA').count(),
                user_scans.filter(exam_type='SUBXIPHOID').count(),
                user_scans.filter(exam_type='PLAX').count(),
                user_scans.filter(exam_type='PSAX').count(),
                user_scans.filter(exam_type='IVC').count(),
                user_scans.filter(exam_type='OB_FIRST').count(),
            ]
            writer.writerow(row)

        return response

    def export_all_view(self, request):
        """Export all scan records directly"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="all_scans_detailed.csv"'

        writer = csv.writer(response)

        header = [
            'ID', 'Username', 'Email', 'Exam Type', 'Scan Context',
            'Performed At', 'Finding', 'Indication', 'Supervisor Present',
            'Supervisor Name', 'Confidence', 'Notes', 'Created At'
        ]
        writer.writerow(header)

        for scan in Scan.objects.all().select_related('user'):
            row = [
                scan.id,
                scan.user.username,
                scan.user.email,
                scan.get_exam_type_display(),
                scan.get_scan_context_display(),
                scan.performed_at,
                scan.get_finding_display(),
                scan.indication,
                'Yes' if scan.supervisor_present else 'No',
                scan.supervisor_name,
                scan.confidence or '',
                scan.notes,
                scan.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            ]
            writer.writerow(row)

        return response

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

