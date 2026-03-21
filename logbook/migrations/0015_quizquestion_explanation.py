from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logbook", "0014_seed_resources"),
    ]

    operations = [
        migrations.AddField(
            model_name="quizquestion",
            name="explanation",
            field=models.TextField(blank=True, help_text="Shown to learners after they submit the quiz to explain the correct answer"),
        ),
    ]
