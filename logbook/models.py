from django.conf import settings
from django.db import models


class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz_slug = models.CharField(max_length=100)  # e.g. "efast-cvc-001"
    answers = models.JSONField(default=dict)      # {"q1": "C", "q2": "A", ...}
    score = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.quiz_slug} {self.score}/{self.total} @ {self.created_at}"

class Scan(models.Model):
    EXAM_CHOICES = [
        ("FAST", "FAST"),
        ("CARDIAC", "Cardiac"),
        ("LUNG", "Lung"),
        ("AORTA", "Aorta"),
        ("IVC", "IVC"),
        ("MSK", "MSK"),
        ("OB", "Obstetrics"),
        ("OTHER", "Other"),
    ]

    FINDING_CHOICES = [
        ("NORMAL", "Normal"),
        ("ABNORMAL", "Abnormal"),
        ("INDETERMINATE", "Indeterminate"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="scans",
    )

    performed_at = models.DateField()

    exam_type = models.CharField(max_length=20, choices=EXAM_CHOICES)

    indication = models.CharField(max_length=200, blank=True)

    finding = models.CharField(max_length=20, choices=FINDING_CHOICES)

    notes = models.TextField(blank=True)

    supervisor_present = models.BooleanField(default=False)

    supervisor_name = models.CharField(
    max_length=100,
    blank=True,
    help_text="Optional: name of supervising staff/resident"
)

    confidence = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Optional: confidence 1–5",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.exam_type} - {self.performed_at}"


class ClinicalCase(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class CaseStep(models.Model):
    case = models.ForeignKey(ClinicalCase, on_delete=models.CASCADE, related_name="steps")
    order = models.PositiveIntegerField()
    content = models.TextField()

    def __str__(self):
        return f"{self.case.title} – Step {self.order}"


class CaseQuestion(models.Model):
    step = models.OneToOneField(CaseStep, on_delete=models.CASCADE, related_name="question")
    prompt = models.TextField()

    def __str__(self):
        return self.prompt[:50]


class CaseChoice(models.Model):
    question = models.ForeignKey(CaseQuestion, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return self.text
