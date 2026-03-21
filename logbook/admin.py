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

from .models import Scan, QuizAttempt, QuizBestScore, QuizQuestion, QuizShortAnswer, ClinicalCase, CaseStep, CaseQuestion, CaseChoice, Resource, POCUSProtocol
from .admin_forms import MassAddScansForm
from .views import QUIZZES


# ── Clinical Cases ────────────────────────────────────────────────────────────

class CaseChoiceInline(admin.TabularInline):
    model = CaseChoice
    extra = 4
    fields = ('text', 'is_correct', 'feedback')


class CaseQuestionInline(admin.StackedInline):
    model = CaseQuestion
    extra = 0
    fields = ('prompt',)


@admin.register(CaseStep)
class CaseStepAdmin(admin.ModelAdmin):
    list_display = ('case', 'order', 'content_preview')
    list_filter = ('case',)
    ordering = ('case', 'order')
    inlines = [CaseQuestionInline]

    def content_preview(self, obj):
        return obj.content[:80] + ('…' if len(obj.content) > 80 else '')
    content_preview.short_description = "Content"


@admin.register(CaseQuestion)
class CaseQuestionAdmin(admin.ModelAdmin):
    list_display = ('prompt_preview', 'step')
    inlines = [CaseChoiceInline]

    def prompt_preview(self, obj):
        return obj.prompt[:80] + ('…' if len(obj.prompt) > 80 else '')
    prompt_preview.short_description = "Prompt"


class CaseStepInline(admin.StackedInline):
    model = CaseStep
    extra = 1
    show_change_link = True
    fields = ('order', 'content')
    ordering = ('order',)


@admin.register(ClinicalCase)
class ClinicalCaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'step_count')
    list_editable = ('is_published',)
    search_fields = ('title', 'description')
    inlines = [CaseStepInline]

    def step_count(self, obj):
        return obj.steps.count()
    step_count.short_description = "Steps"


# ── Resources ─────────────────────────────────────────────────────────────────

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order', 'is_published', 'url_link')
    list_editable = ('order', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'description')
    ordering = ('order', 'title')
    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'description', 'is_published', 'order'),
        }),
        ('Link & Media', {
            'fields': ('url', 'image_url'),
        }),
    )

    def url_link(self, obj):
        from django.utils.html import format_html
        return format_html('<a href="{}" target="_blank">Open</a>', obj.url)
    url_link.short_description = "URL"

    class Media:
        js = ('admin/js/quiz_field_tooltips.js',)


# ── POCUS Protocols ───────────────────────────────────────────────────────────

@admin.register(POCUSProtocol)
class POCUSProtocolAdmin(admin.ModelAdmin):
    list_display = ('name', 'tab_id', 'order', 'is_published')
    list_editable = ('order', 'is_published')
    search_fields = ('name', 'description')
    ordering = ('order',)
    fieldsets = (
        (None, {
            'fields': ('name', 'tab_id', 'icon_class', 'description', 'is_published', 'order'),
        }),
        ('Protocol Content (HTML)', {
            'fields': ('content',),
            'description': 'Paste the full HTML body for this protocol. It will be rendered inside the tab on the Protocols page.',
        }),
    )

    class Media:
        js = ('admin/js/quiz_field_tooltips.js',)


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
        """Export selected quiz attempts as a print-ready HTML report (use browser Print → Save as PDF)."""
        import html as html_module

        rows_html = ""
        for attempt in queryset.select_related("user").order_by("quiz_id", "user__username"):
            answers = attempt.answers or {}
            quiz_data = QUIZZES.get(attempt.quiz_id, {})
            correct_answers = quiz_data.get("questions", {})
            labels = quiz_data.get("question_labels", {})
            short_answer_defs = quiz_data.get("short_answers", {})

            result_text = "PASS" if attempt.percentage >= 70 else "FAIL"
            result_color = "#16a34a" if attempt.percentage >= 70 else "#dc2626"

            rows_html += f"""
<div class="attempt">
  <div class="attempt-header">
    <span class="attempt-name">{html_module.escape(attempt.user.username)} &mdash; {html_module.escape(attempt.quiz_title)}</span>
    <span class="attempt-result" style="color:{result_color};">{result_text}</span>
  </div>
  <div class="attempt-meta">
    Email: {html_module.escape(attempt.user.email or '—')} &nbsp;|&nbsp;
    Date: {attempt.created_at.strftime('%Y-%m-%d %H:%M')} &nbsp;|&nbsp;
    Score: {attempt.score}/{attempt.total} ({attempt.percentage}%)
  </div>
"""
            # Multiple choice table
            if correct_answers:
                mc_keys = sorted(k for k in correct_answers if k.startswith("q"))
                rows_html += """
  <table>
    <thead><tr><th>Q#</th><th>Topic</th><th>Your Answer</th><th>Correct</th><th>Result</th></tr></thead>
    <tbody>
"""
                for key in mc_keys:
                    user_ans = answers.get(key, "—")
                    correct_ans = correct_answers.get(key, "?")
                    is_correct = str(user_ans).upper() == str(correct_ans).upper()
                    result_cell = '<span class="correct">&#10003; Correct</span>' if is_correct else '<span class="wrong">&#10007; Wrong</span>'
                    ans_color = "#16a34a" if is_correct else "#dc2626"
                    rows_html += f"""
      <tr>
        <td class="center">{key.upper()}</td>
        <td>{html_module.escape(labels.get(key, key))}</td>
        <td class="center" style="color:{ans_color};font-weight:bold;">{html_module.escape(str(user_ans))}</td>
        <td class="center">{html_module.escape(str(correct_ans))}</td>
        <td class="center">{result_cell}</td>
      </tr>"""
                rows_html += "\n    </tbody>\n  </table>\n"

            # Short answers
            for sa_key, sa_def in short_answer_defs.items():
                user_sa = answers.get(sa_key, "")
                if user_sa:
                    rows_html += f"""
  <div class="sa-block">
    <div class="sa-prompt"><strong>{sa_key.upper()}</strong> — {html_module.escape(sa_def['prompt'])}</div>
    <div class="sa-response"><em>Response:</em> {html_module.escape(str(user_sa))}</div>
    <div class="sa-sample"><em>Sample answer:</em> {html_module.escape(str(sa_def.get('sample_answer', '')))}</div>
  </div>"""

            rows_html += "\n</div>\n<hr>\n"

        generated = timezone.now().strftime("%Y-%m-%d %H:%M UTC")
        html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>POCUS Portal — Quiz Attempt Report</title>
<style>
  body {{ font-family: Arial, sans-serif; font-size: 11px; color: #111; margin: 24px; }}
  h1 {{ font-size: 16px; color: #1a3c5e; margin-bottom: 2px; }}
  .meta {{ font-size: 10px; color: #555; margin-bottom: 16px; }}
  .attempt {{ margin-bottom: 16px; page-break-inside: avoid; }}
  .attempt-header {{ font-size: 13px; font-weight: bold; color: #1a3c5e; display: flex; justify-content: space-between; }}
  .attempt-result {{ font-weight: bold; }}
  .attempt-meta {{ font-size: 10px; color: #555; margin: 3px 0 6px; }}
  table {{ width: 100%; border-collapse: collapse; margin-bottom: 8px; font-size: 10px; }}
  th {{ background: #1a3c5e; color: #fff; padding: 4px 6px; text-align: left; }}
  td {{ padding: 3px 6px; border-bottom: 1px solid #e2e8f0; }}
  tr:nth-child(even) td {{ background: #f8fafc; }}
  .center {{ text-align: center; }}
  .correct {{ color: #16a34a; font-weight: bold; }}
  .wrong {{ color: #dc2626; font-weight: bold; }}
  .sa-block {{ background: #f8fafc; border-left: 3px solid #cbd5e1; padding: 5px 8px; margin: 4px 0; font-size: 10px; }}
  .sa-prompt {{ font-weight: bold; margin-bottom: 2px; }}
  .sa-sample {{ color: #6b7280; margin-top: 2px; }}
  hr {{ border: none; border-top: 1px solid #cbd5e1; margin: 12px 0; }}
  @media print {{
    body {{ margin: 0; }}
    .no-print {{ display: none; }}
  }}
</style>
</head>
<body>
<div class="no-print" style="margin-bottom:16px;">
  <button onclick="window.print()" style="padding:6px 14px;font-size:13px;cursor:pointer;">&#128438; Print / Save as PDF</button>
</div>
<h1>POCUS Portal &mdash; Quiz Attempt Report</h1>
<div class="meta">Generated: {generated} &nbsp;|&nbsp; {queryset.count()} attempt(s)</div>
<hr>
{rows_html}
</body>
</html>"""

        response = HttpResponse(html_out, content_type="text/html; charset=utf-8")
        return response

    export_quiz_attempts_pdf.short_description = "Export selected attempts to printable report (PDF via browser)"


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
                            # If you're preventing duplicates and one already exists for the day,
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


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz_id', 'key', 'question_preview', 'correct_answer', 'label', 'has_image')
    list_filter = ('quiz_id',)
    list_editable = ('correct_answer',)
    search_fields = ('question_text', 'label')
    ordering = ('quiz_id', 'order')
    fieldsets = (
        (None, {
            'fields': ('quiz_id', 'key', 'order', 'label', 'section_heading')
        }),
        ('Question', {
            'fields': ('question_text', 'image_url'),
        }),
        ('Answer Choices', {
            'fields': ('choice_a', 'choice_b', 'choice_c', 'choice_d', 'choice_e', 'correct_answer'),
            'description': 'Fill in the choices that apply. Leave empty choices blank.',
        }),
    )

    def question_preview(self, obj):
        return obj.question_text[:70] + ('…' if len(obj.question_text) > 70 else '')
    question_preview.short_description = "Question"

    def has_image(self, obj):
        return bool(obj.image_url)
    has_image.boolean = True
    has_image.short_description = "Image?"

    class Media:
        js = ('admin/js/quiz_field_tooltips.js',)

    class Media:
        js = ('admin/js/quiz_field_tooltips.js',)


@admin.register(QuizShortAnswer)
class QuizShortAnswerAdmin(admin.ModelAdmin):
    list_display = ('quiz_id', 'key', 'prompt_preview', 'min_keywords', 'has_image')
    list_filter = ('quiz_id',)
    search_fields = ('prompt', 'keywords')
    ordering = ('quiz_id', 'order')
    fieldsets = (
        (None, {
            'fields': ('quiz_id', 'key', 'order')
        }),
        ('Question', {
            'fields': ('prompt', 'image_url'),
        }),
        ('Scoring', {
            'fields': ('keywords', 'min_keywords', 'sample_answer'),
            'description': 'Keywords are comma-separated. The learner must match at least min_keywords to auto-pass.',
        }),
    )

    def prompt_preview(self, obj):
        return obj.prompt[:70] + ('…' if len(obj.prompt) > 70 else '')
    prompt_preview.short_description = "Prompt"

    def has_image(self, obj):
        return bool(obj.image_url)
    has_image.boolean = True
    has_image.short_description = "Image?"
