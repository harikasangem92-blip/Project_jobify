from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('jobs', '0004_seed_jobroles')]

    operations = [
        migrations.AddField(model_name='jobseekerprofile', name='resume_headline', field=models.CharField(blank=True, max_length=160)),
        migrations.AddField(model_name='jobseekerprofile', name='resume_summary', field=models.TextField(blank=True, max_length=1200)),
        migrations.AddField(model_name='jobseekerprofile', name='education', field=models.TextField(blank=True, help_text='Degrees, institutions, and dates')),
        migrations.AddField(model_name='jobseekerprofile', name='experience', field=models.TextField(blank=True, help_text='Roles, companies, dates, and achievements')),
        migrations.AddField(model_name='jobseekerprofile', name='projects', field=models.TextField(blank=True, help_text='Projects, outcomes, and technologies')),
        migrations.AddField(model_name='jobseekerprofile', name='certifications', field=models.TextField(blank=True)),
        migrations.AddField(model_name='jobseekerprofile', name='portfolio_url', field=models.URLField(blank=True)),
        migrations.AddField(model_name='jobseekerprofile', name='linkedin_url', field=models.URLField(blank=True)),
    ]