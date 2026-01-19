def home(request):
    return render(request, "dashboard.html")
def cases_list(request):
    return render(request, "logbook/cases_list.html")
def pocus_calendar(request):
    return render(request, "logbook/pocus_calendar.html")


def quizzes_list(request):
    return render(request, "logbook/quizzes_list.html")


def resources(request):
    return render(request, "logbook/resources.html")
