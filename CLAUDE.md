# POCUS Portal - Logbook

University of Manitoba POCUS (Point-of-Care Ultrasound) education portal for medical learners. Django web app with quiz system, scan logging, clinical cases, and progress tracking.

## Tech Stack

- **Framework**: Django 4.2.11 / Python 3.11
- **Database**: SQLite (dev), PostgreSQL via `dj-database-url` (prod)
- **Static files**: WhiteNoise
- **PDF generation**: ReportLab
- **Deployment**: Render (render.yaml) and PythonAnywhere

## Project Structure

```
mysite/          — Django project config (settings, urls, wsgi)
logbook/         — Main app (models, views, forms, admin, management commands)
templates/       — All HTML templates (base, registration, logbook/)
static/          — CSS, JS, images, PDFs
```

## Commands

```bash
# Run dev server
python manage.py runserver

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Create admin user
python manage.py create_admin

# Import CCFP users
python manage.py import_ccfp_users

# Populate quiz questions
python manage.py populate_quiz_questions
```

## Key Models

- **Scan** — Logged ultrasound exam with IQ quality scoring (7-field POCUS IQ scale)
- **QuizQuestion / QuizShortAnswer** — DB-driven quiz content (10 quizzes)
- **QuizAttempt / QuizBestScore** — Quiz results and best-score tracking
- **ClinicalCase / CaseStep / CaseQuestion / CaseChoice** — Interactive clinical cases
- **POCUSProtocol** — Protocol reference content (HTML body, admin-editable)
- **Resource** — External learning resources (videos, articles, PDFs)

## Environment Variables

- `SECRET_KEY` — Django secret key
- `DEBUG` — "True"/"False"
- `DATABASE_URL` — PostgreSQL connection string (prod)
- `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` — SMTP for password reset

## Design

Professional medical/academic aesthetic. See DESIGN.md for color palette, typography, and component specs. Uses Inter + Source Sans Pro fonts, medical blue (#0B4F6C) and teal (#2A9D8F) color scheme.
