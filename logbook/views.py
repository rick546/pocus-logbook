from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Avg, F
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from .models import ClinicalCase, CaseStep
from .models import QuizAttempt, QuizBestScore
from .forms import ScanForm
from .models import Scan

User = get_user_model()

# Total number of quizzes available in the curriculum
TOTAL_QUIZZES = 3

# Quiz data
QUIZZES = {
    1: {
        "title": "E-FAST + US-Guided CVC Basics",
        "questions": {
            "q1": "C",
            "q2": "B",
            "q3": "C",
            "q4": "B",
            "q5": "B",
        }
    },
    # Future quizzes will be added here
    # 2: { "title": "Cardiac POCUS Fundamentals", "questions": {...} },
    # 3: { "title": "Lung & Pleural Ultrasound", "questions": {...} },
}

# Keep QUIZ_1 for backward compatibility
QUIZ_1 = QUIZZES[1]

# Quiz home page showing all available quizzes
@login_required
def quizzes_home(request):
    # Get user's best scores for all quizzes
    user_best_scores = {
        score.quiz_id: score
        for score in QuizBestScore.objects.filter(user=request.user)
    }

    # Calculate statistics
    quizzes_completed = len(user_best_scores)
    quizzes_passed = sum(1 for score in user_best_scores.values() if score.passed)

    # Calculate average score
    if user_best_scores:
        avg_score = sum(score.percentage for score in user_best_scores.values()) / len(user_best_scores)
    else:
        avg_score = None

    return render(request, "logbook/quizzes_home.html", {
        "user_best_scores": user_best_scores,
        "quizzes_completed": quizzes_completed,
        "quizzes_passed": quizzes_passed,
        "avg_score": avg_score,
        "total_quizzes": TOTAL_QUIZZES,
    })

# Individual quiz detail page
@login_required
def quiz_detail(request, quiz_id):
    # Check if quiz exists and is available
    if quiz_id not in QUIZZES:
        return render(request, "logbook/quiz_unavailable.html", {"quiz_id": quiz_id})

    quiz = QUIZZES[quiz_id]
    answer_key = quiz["questions"]
    total = len(answer_key)

    submitted_answers = {}
    score = None
    is_new_best = False

    # Get user's previous best score for this quiz
    previous_best = QuizBestScore.objects.filter(user=request.user, quiz_id=quiz_id).first()

    if request.method == "POST":
        submitted_answers = {q: request.POST.get(q) for q in answer_key.keys()}
        score = sum(1 for q, correct in answer_key.items() if submitted_answers.get(q) == correct)

        # Save the quiz attempt
        QuizAttempt.objects.create(
            user=request.user,
            quiz_id=quiz_id,
            quiz_title=quiz["title"],
            answers=submitted_answers,
            score=score,
            total=total,
        )

        # Update or create best score
        best_score, created = QuizBestScore.objects.get_or_create(
            user=request.user,
            quiz_id=quiz_id,
            defaults={
                "quiz_title": quiz["title"],
                "best_score": score,
                "total": total,
                "attempts": 1,
            }
        )

        if not created:
            best_score.attempts += 1
            if score > best_score.best_score:
                best_score.best_score = score
                is_new_best = True
            best_score.save()
        else:
            is_new_best = True

    return render(request, "logbook/quizzes_list.html", {
        "quiz": quiz,
        "quiz_id": quiz_id,
        "answer_key": answer_key,
        "submitted_answers": submitted_answers,
        "score": score,
        "total": total,
        "previous_best": previous_best,
        "is_new_best": is_new_best,
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
        .filter(scans__isnull=False)
        .annotate(total=Count("scans"))
        .order_by("-total", "username")[:10]
    )

    # Quiz progress for authenticated users
    quiz_progress = None
    quizzes_completed = 0
    quiz_percentage = 0

    if request.user.is_authenticated:
        # Count quizzes where user has passed (70% or higher)
        user_best_scores = QuizBestScore.objects.filter(user=request.user)
        quizzes_completed = user_best_scores.filter(best_score__gte=models.F('total') * 0.7).count()

        # Alternative: count any quiz attempted (regardless of score)
        # quizzes_completed = user_best_scores.count()

        quiz_percentage = round((quizzes_completed / TOTAL_QUIZZES) * 100) if TOTAL_QUIZZES > 0 else 0

        quiz_progress = {
            "completed": quizzes_completed,
            "total": TOTAL_QUIZZES,
            "percentage": quiz_percentage,
        }

    return render(request, "home.html", {
        "leaderboard": leaderboard,
        "quiz_progress": quiz_progress,
    })


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

