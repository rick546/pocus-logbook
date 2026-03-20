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

    CONTEXT_CHOICES = [
        ("ACADEMIC", "Academic Half Day"),
        ("SELF", "Self Logged"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="scans",
    )

    performed_at = models.DateField()

    exam_type = models.CharField(max_length=20, choices=EXAM_CHOICES)

    scan_context = models.CharField(
        max_length=10,
        choices=CONTEXT_CHOICES,
        default="SELF",
        verbose_name="Scan Context",
        help_text="Where was this scan performed?",
    )

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
    media_url = models.URLField(blank=True, help_text="Optional YouTube embed URL or direct video/image URL to display above the question")

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


class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('video', 'Video'),
        ('article', 'Article'),
        ('pdf', 'PDF / Document'),
        ('guideline', 'Guideline'),
        ('link', 'External Link'),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='link')
    description = models.TextField(blank=True)
    url = models.URLField(help_text="Link to the resource (article, video, PDF, etc.)")
    image_url = models.URLField(blank=True, help_text="Optional thumbnail image URL to display on the card")
    order = models.PositiveIntegerField(default=0, help_text="Display order — lower numbers appear first")
    is_published = models.BooleanField(default=True, help_text="Uncheck to hide from learners")

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Resource"
        verbose_name_plural = "Resources"

    def __str__(self):
        return self.title


class POCUSProtocol(models.Model):
    name = models.CharField(max_length=100, help_text="Protocol name shown on the tab (e.g. 'FAST Scan')")
    tab_id = models.SlugField(max_length=50, unique=True, help_text="URL-safe tab ID, no spaces (e.g. 'fast', 'lung', 'cardiac')")
    icon_class = models.CharField(max_length=60, blank=True, default='fas fa-circle', help_text="Font Awesome icon class (e.g. 'fas fa-search', 'fas fa-lungs', 'fas fa-heart')")
    description = models.TextField(blank=True, help_text="Short subtitle shown below the protocol heading")
    content = models.TextField(blank=True, help_text="Full protocol body as HTML — paste your HTML here, it will be rendered directly on the page")
    order = models.PositiveIntegerField(default=0, help_text="Tab order — lower numbers appear first (leftmost)")
    is_published = models.BooleanField(default=True, help_text="Uncheck to hide this protocol from learners")

    class Meta:
        ordering = ['order']
        verbose_name = "POCUS Protocol"
        verbose_name_plural = "POCUS Protocols"

    def __str__(self):
        return self.name


class QuizQuestion(models.Model):
    quiz_id = models.PositiveIntegerField(db_index=True, help_text="Which quiz this question belongs to: 1 = E-FAST + CVC Basics, 2 = POCUS Session #1, 3 = Focused Echo")
    key = models.CharField(max_length=10, help_text="Unique identifier within the quiz (e.g. q1, q2, q3). New questions should continue the sequence — if the quiz has q1-q5, use q6.")
    order = models.PositiveIntegerField(default=0, help_text="Display position in the quiz. 1 = shown first. New questions should use the next available number (e.g. if quiz has 5 questions, enter 6).")
    section_heading = models.CharField(max_length=200, blank=True, help_text="Optional section heading shown before this question (e.g. 'Ultrasound Physics Questions')")
    question_text = models.TextField()
    choice_a = models.CharField(max_length=500, blank=True)
    choice_b = models.CharField(max_length=500, blank=True)
    choice_c = models.CharField(max_length=500, blank=True)
    choice_d = models.CharField(max_length=500, blank=True)
    choice_e = models.CharField(max_length=500, blank=True)
    correct_answer = models.CharField(max_length=1, help_text="A, B, C, D, or E")
    image_url = models.URLField(blank=True, help_text="Optional POCUS image URL displayed above this question")
    label = models.CharField(max_length=200, blank=True, help_text="Short topic label used in analytics")

    class Meta:
        unique_together = ['quiz_id', 'key']
        ordering = ['quiz_id', 'order']
        verbose_name = "Quiz Question"
        verbose_name_plural = "Quiz Questions"

    def __str__(self):
        return f"Quiz {self.quiz_id} — {self.key.upper()}: {self.question_text[:60]}"

    def get_choices(self):
        choices = []
        for letter, text in [('A', self.choice_a), ('B', self.choice_b), ('C', self.choice_c), ('D', self.choice_d), ('E', self.choice_e)]:
            if text:
                choices.append((letter, text))
        return choices


class QuizShortAnswer(models.Model):
    quiz_id = models.PositiveIntegerField(db_index=True, help_text="Which quiz this question belongs to: 1 = E-FAST + CVC Basics, 2 = POCUS Session #1, 3 = Focused Echo")
    key = models.CharField(max_length=10, help_text="Unique identifier within the quiz (e.g. sa1, sa2, sa3). New questions should continue the sequence.")
    order = models.PositiveIntegerField(default=0, help_text="Display position in the quiz. 1 = shown first. New questions should use the next available number.")
    prompt = models.TextField()
    sample_answer = models.TextField(blank=True)
    keywords = models.TextField(blank=True, help_text="Comma-separated keywords for auto-scoring")
    min_keywords = models.PositiveIntegerField(default=2)
    image_url = models.URLField(blank=True, help_text="Optional POCUS image URL displayed with this question")

    class Meta:
        unique_together = ['quiz_id', 'key']
        ordering = ['quiz_id', 'order']
        verbose_name = "Quiz Short Answer"
        verbose_name_plural = "Quiz Short Answers"

    def __str__(self):
        return f"Quiz {self.quiz_id} — {self.key.upper()}: {self.prompt[:60]}"

    def keywords_list(self):
        return [k.strip() for k in self.keywords.split(',') if k.strip()]
