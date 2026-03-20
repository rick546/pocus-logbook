import csv
import io
from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count, Q
from django.urls import path
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse

from .models import Scan, QuizAttempt, QuizBestScore
from .admin_forms import MassAddScansForm
from .views import QUIZZES

from django.contrib import admin
from .models import ClinicalCase, CaseStep, CaseQuestion, CaseChoice

admin.site.register(ClinicalCase)
admin.site.register(CaseStep)
admin.site.register(CaseQuestion)
admin.site.register(CaseChoice)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "quiz_title", "score", "total", "percentage_display", "passed_display", "created_at")
    list_filter = ("quiz_id", "quiz_title")
    search_fields = ("user__username", "user__email")
    ordering = ("-created_at",)
    readonly_fields = ("user", "quiz_id", "quiz_title", "answers", "score", "total", "created_at")
    actions = ["export_quiz_scores_csv", "export_quiz_attempts_pdf"]

    def percentage_display(self, obj):
        return f"{obj.percentage}%"
    percentage_display.short_description = "Score %"

    def passed_display(self, obj):
        return "✓ Pass" if obj.percentage >= 70 else "✗ Fail"
    passed_display.short_description = "Result"

    def export_quiz_scores_csv(self, request, queryset):
        """Export selected quiz attempts including short answers to CSV."""
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="quiz_scores.csv"'
        writer = csv.writer(response)

        writer.writerow([
            "Username", "Email", "Quiz", "MC Score", "Total MC Qs",
            "Score %", "Result", "SA1 Response", "SA2 Response", "SA3 Response",
            "Date Completed",
        ])

        for attempt in queryset.select_related("user"):
            answers = attempt.answers or {}
            writer.writerow([
                attempt.user.username,
                attempt.user.email,
                attempt.quiz_title,
                attempt.score,
                attempt.total,
                f"{attempt.percentage}%",
                "Pass" if attempt.percentage >= 70 else "Fail",
                answers.get("sa1", ""),
                answers.get("sa2", ""),
                answers.get("sa3", ""),
                attempt.created_at.strftime("%Y-%m-%d %H:%M"),
            ])

        self.message_user(request, f"Exported {queryset.count()} quiz attempt(s).")
        return response

    export_quiz_scores_csv.short_description = "Export selected attempts to CSV"

    def export_quiz_attempts_pdf(self, request, queryset):
        """Export selected quiz attempts as a detailed PDF showing correct/incorrect answers."""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
            from reportlab.lib.enums import TA_CENTER, TA_LEFT
        except ImportError:
            self.message_user(request, "reportlab is not installed. Run: pip install reportlab", level="error")
            return

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                rightMargin=0.75*inch, leftMargin=0.75*inch,
                                topMargin=0.75*inch, bottomMargin=0.75*inch)

        styles = getSampleStyleSheet()
        style_title = ParagraphStyle("title", parent=styles["Heading1"], fontSize=16, spaceAfter=4, textColor=colors.HexColor("#1a3c5e"))
        style_h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=12, spaceAfter=4, textColor=colors.HexColor("#1a3c5e"))
        style_normal = styles["Normal"]
        style_small = ParagraphStyle("small", parent=styles["Normal"], fontSize=8)
        style_correct = ParagraphStyle("correct", parent=styles["Normal"], textColor=colors.HexColor("#16a34a"), fontSize=9)
        style_wrong = ParagraphStyle("wrong", parent=styles["Normal"], textColor=colors.HexColor("#dc2626"), fontSize=9)

        story = []
        story.append(Paragraph("POCUS Portal — Quiz Attempt Report", style_title))
        story.append(Paragraph(f"Generated: {timezone.now().strftime('%Y-%m-%d %H:%M UTC')}", style_small))
        story.append(Spacer(1, 0.2*inch))

        for attempt in queryset.select_related("user").order_by("quiz_id", "user__username"):
            answers = attempt.answers or {}
            quiz_data = QUIZZES.get(attempt.quiz_id, {})
            correct_answers = quiz_data.get("questions", {})
            labels = quiz_data.get("question_labels", {})
            short_answer_defs = quiz_data.get("short_answers", {})

            # Attempt header
            result_text = "PASS" if attempt.percentage >= 70 else "FAIL"
            result_color = colors.HexColor("#16a34a") if attempt.percentage >= 70 else colors.HexColor("#dc2626")

            story.append(Paragraph(f"{attempt.user.username} — {attempt.quiz_title}", style_h2))
            story.append(Paragraph(
                f"Email: {attempt.user.email or '—'}  |  "
                f"Date: {attempt.created_at.strftime('%Y-%m-%d %H:%M')}  |  "
                f"Score: {attempt.score}/{attempt.total} ({attempt.percentage}%)  |  "
                f"<font color='{'#16a34a' if attempt.percentage >= 70 else '#dc2626'}'><b>{result_text}</b></font>",
                style_normal
            ))
            story.append(Spacer(1, 0.1*inch))

            # Multiple choice table
            if correct_answers:
                mc_keys = [k for k in correct_answers if k.startswith("q")]
                table_data = [["Q#", "Topic", "User's Answer", "Correct Answer", "Result"]]
                for key in sorted(mc_keys):
                    user_ans = answers.get(key, "—")
                    correct_ans = correct_answers.get(key, "?")
                    is_correct = str(user_ans).upper() == str(correct_ans).upper()
                    result_cell = Paragraph("✓ Correct", style_correct) if is_correct else Paragraph("✗ Wrong", style_wrong)
                    user_cell = Paragraph(
                        f"<font color='{'#16a34a' if is_correct else '#dc2626'}'>{user_ans}</font>",
                        style_normal
                    )
                    table_data.append([
                        key.upper(),
                        Paragraph(labels.get(key, key), style_small),
                        user_cell,
                        correct_ans,
                        result_cell,
                    ])

                mc_table = Table(table_data, colWidths=[0.5*inch, 2.8*inch, 1.1*inch, 1.1*inch, 1.0*inch])
                mc_table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3c5e")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (0, 0), (0, -1), "CENTER"),
                    ("ALIGN", (2, 0), (3, -1), "CENTER"),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]))
                story.append(mc_table)
                story.append(Spacer(1, 0.1*inch))

            # Short answers
            for sa_key, sa_def in short_answer_defs.items():
                user_sa = answers.get(sa_key, "")
                if user_sa:
                    story.append(Paragraph(f"<b>{sa_key.upper()} — {sa_def['prompt'][:80]}...</b>", style_small))
                    story.append(Paragraph(f"Response: {user_sa}", style_small))
                    story.append(Paragraph(f"Sample answer: {sa_def.get('sample_answer', '')}", ParagraphStyle("sample", parent=style_small, textColor=colors.HexColor("#6b7280"))))
                    story.append(Spacer(1, 0.05*inch))

            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1")))
            story.append(Spacer(1, 0.15*inch))

        doc.build(story)
        buffer.seek(0)
        response = HttpResponse(buffer, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="quiz_attempts.pdf"'
        return response

    export_quiz_attempts_pdf.short_description = "Export selected attempts to PDF (with correct/incorrect)"


@admin.register(QuizBestScore)
class QuizBestScoreAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz_title", "best_score", "total", "percentage_display", "passed_display", "attempts", "last_attempt")
    list_filter = ("quiz_id", "quiz_title")
    search_fields = ("user__username", "user__email")
    ordering = ("quiz_id", "user__username")
    readonly_fields = ("user", "quiz_id", "quiz_title", "best_score", "total", "attempts", "last_attempt")

    def percentage_display(self, obj):
        return f"{obj.percentage}%"
    percentage_display.short_description = "Best %"

    def passed_display(self, obj):
        return "✓ Pass" if obj.passed else "✗ Fail"
    passed_display.short_description = "Passed"

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

