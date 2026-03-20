from .models import ClinicalCase, CaseStep  # make sure these are imported
from django.urls import path
from . import views


def case_step(request, case_id, step_order):
    case = get_object_or_404(ClinicalCase, id=case_id)
    step = get_object_or_404(CaseStep, case=case, order=step_order)
    return render(request, "logbook/case_step.html", {"case": case, "step": step})


urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("calendar/", views.pocus_calendar, name="pocus_calendar"),
    path("quizzes/", views.quizzes_home, name="quizzes_list"),
    path("quizzes/<int:quiz_id>/", views.quiz_detail, name="quiz_detail"),
    path("resources/", views.resources, name="resources"),
    path("protocols/", views.protocols, name="protocols"),
    path("faculty-evaluation/", views.faculty_evaluation, name="faculty_evaluation"),
    path("search/", views.search, name="search"),
    path("bundles/<slug:bundle>/add/", views.add_scan_bundle, name="add_scan_bundle"),
    path("batch-add/", views.batch_add_scans, name="batch_add_scans"),
    path("logbook/new/", views.scan_create, name="scan_create"),
    path("logbook/", views.my_scans, name="my_scans"),
    path("logbook/<int:pk>/edit/", views.scan_edit, name="scan_edit"),
    path("logbook/<int:pk>/delete/", views.scan_delete, name="scan_delete"),
    path("cases/", views.cases_list, name="cases_list"),
    path("cases/<int:case_id>/step/<int:step_order>/", views.case_step, name="case_step"),
    path("badges/", views.badges, name="badges"),
    path("admin/scans/", views.scan_totals, name="scan_totals"),
    path("admin/quiz-analytics/", views.quiz_analytics, name="quiz_analytics"),
]

