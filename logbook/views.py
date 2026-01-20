from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from .models import ClinicalCase, CaseStep
from .models import QuizAttempt
from .forms import ScanForm
from .models import Scan

User = get_user_model()

dUser = get_user_model()


QUIZ_1 = {
    "title": "E-FAST + US-Guided CVC Basics",
    "questions": {
        "q1": "C",
        "q2": "B",
        "q3": "C",
        "q4": "B",
        "q5": "B",
    }
}

# Quiz home page showing all available quizzes
@login_required
def quizzes_home(request):
    return render(request, "logbook/quizzes_home.html")

# Individual quiz detail page
@login_required
def quiz_detail(request, quiz_id):
    # For now, only quiz 1 is available
    if quiz_id != 1:
        return render(request, "logbook/quiz_unavailable.html", {"quiz_id": quiz_id})

    answer_key = QUIZ_1["questions"]
    total = len(answer_key)

    submitted_answers = {}
    score = None

    if request.method == "POST":
        submitted_answers = {q: request.POST.get(q) for q in answer_key.keys()}
        score = sum(1 for q, correct in answer_key.items() if submitted_answers.get(q) == correct)

    return render(request, "logbook/quizzes_list.html", {
        "quiz": QUIZ_1,
        "answer_key": answer_key,
        "submitted_answers": submitted_answers,
        "score": score,
        "total": total,
    })


def case_step(request, case_id, step_order):
    case = get_object_or_404(ClinicalCase, id=case_id)
    step = get_object_or_404(CaseStep, case=case, order=step_order)

    return render(
        request,
        "logbook/case_step.html",
        {"case": case, "step": step}
    )

def home(request):
    leaderboard = (
        User.objects
        .filter(scans__isnull=False)          # ✅ correct related_name
        .annotate(total=Count("scans"))
        .order_by("-total", "username")[:10]
    )
    return render(request, "home.html", {"leaderboard": leaderboard})


@login_required
def scan_create(request):
    if request.method == "POST":
        form = ScanForm(request.POST)
        if form.is_valid():
            scan = form.save(commit=False)
            scan.user = request.user
            scan.save()
            return redirect("my_scans")
    else:
        form = ScanForm()

    return render(request, "logbook/scan_form.html", {"form": form})


@login_required
def scan_edit(request, pk):
    scan = get_object_or_404(Scan, pk=pk, user=request.user)

    if request.method == "POST":
        form = ScanForm(request.POST, instance=scan)
        if form.is_valid():
            form.save()
            return redirect("my_scans")
    else:
        form = ScanForm(instance=scan)

    return render(request, "logbook/scan_form.html", {"form": form, "is_edit": True})


@login_required
def scan_delete(request, pk):
    scan = get_object_or_404(Scan, pk=pk, user=request.user)

    if request.method == "POST":
        scan.delete()
        return redirect("my_scans")

    return render(request, "logbook/scan_confirm_delete.html", {"scan": scan})


@login_required
def my_scans(request):
    scans = Scan.objects.filter(user=request.user).order_by("-performed_at", "-created_at")

    counts = (
        Scan.objects.filter(user=request.user)
        .values("exam_type")
        .annotate(total=Count("id"))
        .order_by("exam_type")
    )

    return render(request, "logbook/my_scans.html", {"scans": scans, "counts": counts})

@staff_member_required
def scan_totals(request):
    total_scans = Scan.objects.count()

    totals_by_user = (
        Scan.objects.values("user__username")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    totals_by_exam = (
        Scan.objects.values("exam_type")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    return render(
        request,
        "logbook/scan_totals.html",
        {
            "total_scans": total_scans,
            "totals_by_user": totals_by_user,
            "totals_by_exam": totals_by_exam,
        },
    )

from .models import ClinicalCase   # add this at the top if not already imported

def cases_list(request):
    feedback = None

    if request.method == "POST":
        answer = request.POST.get("answer")
        if answer == "B":
            feedback = "✅ Correct. Bilateral diffuse B-lines with pleural effusions and a smooth pleural line is most consistent with cardiogenic pulmonary edema."
        elif answer:
            feedback = "❌ Not quite. Re-check for bilateral diffuse B-lines, a smooth pleural line, and pleural effusions—these findings point toward pulmonary edema."

    return render(request, "logbook/cases_example.html", {"feedback": feedback})


def case_step(request, case_id, step_order):
    case = get_object_or_404(ClinicalCase, id=case_id)
    step = get_object_or_404(CaseStep, case=case, order=step_order)
    return render(request, "logbook/case_step.html", {"case": case, "step": step})


def pocus_calendar(request):
    return render(request, "logbook/pocus_calendar.html")


def resources(request):
    return render(request, "logbook/resources.html")

from django.utils import timezone
from django.views.decorators.http import require_POST

@login_required
@require_POST
def add_scan_bundle(request, bundle):
    bundles = {
        "core_pocus": ["Cardiac", "Lung", "eFAST", "Aorta", "IVC"],
        "trauma_pack": ["eFAST", "Cardiac", "Lung"],
        "shock_pack": ["Cardiac", "IVC", "Aorta"],
        "resp_pack": ["Lung", "Pleura"],
    }

    exam_types = bundles.get(bundle)
    if not exam_types:
        return redirect("home")

    today = timezone.localdate()

    for exam in exam_types:
        Scan.objects.get_or_create(
            user=request.user,
            exam_type=exam,
            performed_at=today,
        )

    return redirect("my_scans")

