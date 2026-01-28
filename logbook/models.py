from django.conf import settings
from django.db import models


class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_attempts")
    quiz_id = models.PositiveIntegerField(default=1)  # Quiz number (1, 2, 3, etc.)
    quiz_title = models.CharField(max_length=200, blank=True, default="")
    answers = models.JSONField(default=dict)      # {"q1": "C", "q2": "A", ...}
    score = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - Quiz {self.quiz_id}: {self.score}/{self.total} @ {self.created_at}"

    @property
    def percentage(self):
        if self.total == 0:
            return 0
        return round((self.score / self.total) * 100)


class QuizBestScore(models.Model):
    """Tracks the best score for each user on each quiz"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_best_scores")
    quiz_id = models.PositiveIntegerField()
    quiz_title = models.CharField(max_length=200, blank=True)
    best_score = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    attempts = models.PositiveIntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'quiz_id']
        ordering = ['quiz_id']

    def __str__(self):
        return f"{self.user} - Quiz {self.quiz_id} Best: {self.best_score}/{self.total}"

    @property
    def percentage(self):
        if self.total == 0:
            return 0
        return round((self.best_score / self.total) * 100)

    @property
    def passed(self):
        """Consider 70% or higher as passed"""
        return self.percentage >= 70

class Scan(models.Model):
    EXAM_CHOICES = [
        ("RUQ", "RUQ Abdomen"),
        ("LUQ", "LUQ Abdomen"),
        ("AORTA", "Aorta"),
        ("SUBXIPHOID", "Subxiphoid (Cardiac)"),
        ("PLAX", "Parasternal Long Axis (Cardiac)"),
        ("PSAX", "Parasternal Short Axis (Cardiac)"),
        ("IVC", "IVC"),
        ("OB_FIRST", "First-Trimester (Obstetrics)"),
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

    # POCUS IQ Scale fields (optional survey)
    IQ_SCALE_CHOICES = [
        (0, "0 - Inadequate"),
        (1, "1 - Adequate"),
        (2, "2 - Ideal/Excellent"),
    ]

    iq_probe_choice = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=IQ_SCALE_CHOICES,
        verbose_name="Technical Skill: Probe Choice",
        help_text="0=Inadequate for visualization, 2=Ideal",
    )

    iq_depth = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=IQ_SCALE_CHOICES,
        verbose_name="Technical Skill: Depth",
        help_text="0=Inadequate for visualization, 2=Ideal",
    )

    iq_gain_presets = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=IQ_SCALE_CHOICES,
        verbose_name="Technical Skill: Gain/Presets",
        help_text="0=Inadequate for visualization, 2=Ideal",
    )

    iq_probe_control = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=IQ_SCALE_CHOICES,
        verbose_name="Scanning Skill: Probe Control",
        help_text="0=Poor probe control, 2=Excellent probe control",
    )

    iq_anatomy_landmarks = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=IQ_SCALE_CHOICES,
        verbose_name="Scanning Skill: Anatomy/Landmarks",
        help_text="0=Poor demonstration, 2=Excellent demonstration",
    )

    iq_labelling = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=IQ_SCALE_CHOICES,
        verbose_name="Interpretability: Labelling",
        help_text="0=Inadequate labeling, 2=Ideal labelling",
    )

    iq_completeness = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=IQ_SCALE_CHOICES,
        verbose_name="Interpretability: Completeness",
        help_text="0=Inadequate views, 2=Ideal views",
    )

    iq_comments = models.TextField(
        blank=True,
        verbose_name="IQ Scale Comments",
        help_text="Optional comments on image quality",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def iq_total_score(self):
        """Calculate total POCUS IQ score if any fields are filled"""
        fields = [
            self.iq_probe_choice,
            self.iq_depth,
            self.iq_gain_presets,
            self.iq_probe_control,
            self.iq_anatomy_landmarks,
            self.iq_labelling,
            self.iq_completeness,
        ]
        filled = [f for f in fields if f is not None]
        if not filled:
            return None
        return sum(filled)

    @property
    def iq_max_score(self):
        """Maximum possible score based on filled fields"""
        fields = [
            self.iq_probe_choice,
            self.iq_depth,
            self.iq_gain_presets,
            self.iq_probe_control,
            self.iq_anatomy_landmarks,
            self.iq_labelling,
            self.iq_completeness,
        ]
        filled = [f for f in fields if f is not None]
        return len(filled) * 2 if filled else None

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
