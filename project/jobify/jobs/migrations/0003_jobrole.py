from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('jobs', '0002_viewedjob'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('required_skills', models.TextField(help_text='Enter skills separated by commas')),
            ],
            options={
                'db_table': 'job_role',
                'verbose_name': 'Job Role',
                'verbose_name_plural': 'Job Roles',
            },
        ),
    ]