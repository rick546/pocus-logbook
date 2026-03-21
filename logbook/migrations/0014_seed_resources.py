from django.db import migrations


RESOURCES = [
    {
        "title": "FOCUS Introduction — Utah Anesthesia Echo",
        "category": "article",
        "description": "Overview of Focused Cardiac Ultrasound (FOCUS) for point-of-care use.",
        "url": "https://echo.anesthesia.med.utah.edu/focus-intro/",
        "order": 10,
    },
    {
        "title": "FOCUS: Parasternal Long Axis (PLAX) — Utah Anesthesia Echo",
        "category": "article",
        "description": "Step-by-step guide to acquiring and interpreting the parasternal long-axis view.",
        "url": "https://echo.anesthesia.med.utah.edu/focus-how-to-parasternal-long-axis/",
        "order": 11,
    },
    {
        "title": "FOCUS: Parasternal Short Axis (PSAX) — Utah Anesthesia Echo",
        "category": "article",
        "description": "Step-by-step guide to acquiring and interpreting the parasternal short-axis view.",
        "url": "https://echo.anesthesia.med.utah.edu/focus-how-to-parasternal-short-axis/",
        "order": 12,
    },
    {
        "title": "Hematology POCUS — MMH Heme",
        "category": "article",
        "description": "POCUS resources for hematology applications.",
        "url": "https://www.mmheme.org/new-page-5",
        "order": 20,
    },
    {
        "title": "E-FAST Ultrasound Exam: Step-by-Step Guide — POCUS 101",
        "category": "article",
        "description": "Comprehensive guide to performing and interpreting the Extended Focused Assessment with Sonography for Trauma (E-FAST).",
        "url": "https://www.pocus101.com/efast-ultrasound-exam-made-easy-step-by-step-guide/",
        "order": 30,
    },
    {
        "title": "POCUS Video Tutorial — YouTube",
        "category": "video",
        "description": "Point-of-care ultrasound video tutorial.",
        "url": "https://www.youtube.com/watch?v=y2gsW4n6XtY",
        "order": 40,
    },
    {
        "title": "POCUS Video Tutorial #2 — YouTube",
        "category": "video",
        "description": "Point-of-care ultrasound video tutorial.",
        "url": "https://www.youtube.com/watch?v=Ym6rx2X-gFY",
        "order": 41,
    },
    {
        "title": "POCUS Presentation Slides — Google Slides",
        "category": "pdf",
        "description": "Slide deck covering key POCUS concepts and applications.",
        "url": "https://docs.google.com/presentation/d/12H9XU9-ifXJlmI38a_fm7cAjT1n-o-iBu6bl8ke4-ns/edit?usp=sharing",
        "order": 50,
    },
]


def seed_resources(apps, schema_editor):
    Resource = apps.get_model("logbook", "Resource")
    for data in RESOURCES:
        if not Resource.objects.filter(url=data["url"]).exists():
            Resource.objects.create(**data)


def unseed_resources(apps, schema_editor):
    Resource = apps.get_model("logbook", "Resource")
    urls = [r["url"] for r in RESOURCES]
    Resource.objects.filter(url__in=urls).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("logbook", "0013_seed_dyspnea_case"),
    ]

    operations = [
        migrations.RunPython(seed_resources, unseed_resources),
    ]
