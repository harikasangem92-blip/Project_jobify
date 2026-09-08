from django.db import migrations


ROLES = [
    ('Software Engineer', 'Python, Django, REST APIs, SQL, Git, Docker, Algorithms'),
    ('Frontend Developer', 'HTML, CSS, JavaScript, React, Responsive Design, Git'),
    ('Data Scientist', 'Python, Pandas, NumPy, SQL, Statistics, Machine Learning'),
    ('DevOps Engineer', 'Linux, Docker, Kubernetes, CI/CD, Terraform, AWS'),
    ('QA Engineer', 'Test Automation, Selenium, API Testing, Python, CI/CD'),
]


def seed_roles(apps, schema_editor):
    JobRole = apps.get_model('jobs', 'JobRole')
    JobRole.objects.bulk_create([
        JobRole(title=title, required_skills=skills)
        for title, skills in ROLES
    ])


def remove_roles(apps, schema_editor):
    JobRole = apps.get_model('jobs', 'JobRole')
    JobRole.objects.filter(title__in=[title for title, _ in ROLES]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('jobs', '0003_jobrole'),
    ]

    operations = [migrations.RunPython(seed_roles, remove_roles)]