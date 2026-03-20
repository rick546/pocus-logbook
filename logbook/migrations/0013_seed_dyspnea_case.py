from django.db import migrations


def seed_case(apps, schema_editor):
    ClinicalCase = apps.get_model('logbook', 'ClinicalCase')
    CaseStep = apps.get_model('logbook', 'CaseStep')
    CaseQuestion = apps.get_model('logbook', 'CaseQuestion')
    CaseChoice = apps.get_model('logbook', 'CaseChoice')

    case, created = ClinicalCase.objects.get_or_create(
        title="Clinical Case: Dyspnea — Lung Ultrasound (LUS)",
        defaults={
            "description": "Review the ultrasound clip and answer questions about lung ultrasound findings in a patient presenting with acute dyspnea.",
            "is_published": True,
        }
    )

    if not created:
        return  # already seeded

    step = CaseStep.objects.create(
        case=case,
        order=1,
        content="A patient presents with acute dyspnea. Review the lung ultrasound clip below and identify the findings.",
        media_url="https://www.youtube.com/embed/m9s5AD_lBkY",
    )

    question = CaseQuestion.objects.create(
        step=step,
        prompt="What do the LUS images reveal, and what is the most likely etiology of the patient's dyspnea?",
    )

    choices = [
        {
            "text": "A) Patchy B-lines and asymmetrical consolidation, suggestive of possible pneumonia",
            "is_correct": False,
            "feedback": "❌ Not quite. Pneumonia typically shows asymmetric, patchy B-lines and subpleural consolidation — not the bilateral diffuse pattern seen here.",
        },
        {
            "text": "B) Bilateral diffuse B-lines, smooth pleural line, and bilateral pleural effusions, suggestive of pulmonary edema",
            "is_correct": True,
            "feedback": "✅ Correct! Bilateral diffuse B-lines with pleural effusions and a smooth pleural line is most consistent with cardiogenic pulmonary edema.",
        },
        {
            "text": "C) Right-sided pneumothorax",
            "is_correct": False,
            "feedback": "❌ Incorrect. Pneumothorax shows absent lung sliding and A-lines (or barcode sign on M-mode) — not B-lines or effusions.",
        },
        {
            "text": "D) Diffuse B-lines with ragged pleural line and bilateral consolidations, suggestive of possible ARDS",
            "is_correct": False,
            "feedback": "❌ Not quite. ARDS shows an irregular/ragged pleural line and non-homogeneous B-lines. The smooth pleural line here points to a hydrostatic (cardiogenic) cause.",
        },
    ]

    for c in choices:
        CaseChoice.objects.create(question=question, **c)


def unseed_case(apps, schema_editor):
    ClinicalCase = apps.get_model('logbook', 'ClinicalCase')
    ClinicalCase.objects.filter(title="Clinical Case: Dyspnea — Lung Ultrasound (LUS)").delete()


class Migration(migrations.Migration):

    dependencies = [
        ('logbook', '0012_casestep_media_url'),
    ]

    operations = [
        migrations.RunPython(seed_case, unseed_case),
    ]
