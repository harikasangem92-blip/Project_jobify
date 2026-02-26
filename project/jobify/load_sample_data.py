"""
Sample data loader for Jobify
Run: python manage.py shell < load_sample_data.py
"""

from django.utils import timezone
from datetime import timedelta
from jobs.models import CustomUser, JobSeekerProfile, EmployerProfile, Job

print("Creating sample data...")

# Create sample job seeker
jobseeker = CustomUser.objects.create_user(
    username='jobseeker@example.com',
    email='jobseeker@example.com',
    password='password123',
    first_name='John',
    last_name='Doe',
    role='job_seeker',
    phone='+1-555-0101'
)

JobSeekerProfile.objects.create(
    user=jobseeker,
    skills='Python, Django, JavaScript, React, PostgreSQL',
    bio='Experienced full-stack developer with 5 years in web development',
    experience_years=5,
    location='New York, NY'
)

print(f"✓ Created job seeker: {jobseeker.email}")

# Create sample employer
employer = CustomUser.objects.create_user(
    username='employer@example.com',
    email='employer@example.com',
    password='password123',
    first_name='Jane',
    last_name='Smith',
    role='employer',
    phone='+1-555-0102'
)

EmployerProfile.objects.create(
    user=employer,
    company_name='Tech Innovations Inc',
    company_description='Leading software development company specializing in web and mobile applications',
    company_website='https://techinnovations.com',
    company_size='51-200',
    location='San Francisco, CA',
    is_verified=True
)

print(f"✓ Created employer: {employer.email}")

# Create sample jobs
jobs_data = [
    {
        'title': 'Senior Django Developer',
        'description': 'We are looking for an experienced Django developer to join our team. You will be responsible for developing and maintaining our web applications.\n\nResponsibilities:\n- Develop scalable Django applications\n- Write clean, maintainable code\n- Collaborate with team members\n- Participate in code reviews',
        'required_skills': 'Django, Python, PostgreSQL, REST APIs, Git',
        'salary_min': 100000,
        'salary_max': 150000,
        'location': 'San Francisco, CA',
        'job_type': 'full_time',
        'experience_required': '5+ years',
        'vacancies': 2,
    },
    {
        'title': 'Frontend React Developer',
        'description': 'Join our dynamic team as a React Frontend Developer. You will create beautiful and responsive user interfaces.\n\nWhat we offer:\n- Competitive salary\n- Remote work options\n- Professional development\n- Great team culture',
        'required_skills': 'React, JavaScript, HTML, CSS, TypeScript',
        'salary_min': 80000,
        'salary_max': 120000,
        'location': 'Remote',
        'job_type': 'remote',
        'experience_required': '3+ years',
        'vacancies': 3,
    },
    {
        'title': 'Full Stack Developer Internship',
        'description': 'Great opportunity for students to gain real-world experience. We will mentor you in full-stack development.',
        'required_skills': 'Python, JavaScript, HTML, CSS',
        'salary_min': 20000,
        'salary_max': 30000,
        'location': 'New York, NY',
        'job_type': 'internship',
        'experience_required': 'Entry-level',
        'vacancies': 5,
    },
    {
        'title': 'DevOps Engineer',
        'description': 'We need a DevOps engineer to manage our cloud infrastructure and CI/CD pipelines.',
        'required_skills': 'Docker, Kubernetes, AWS, CI/CD, Linux',
        'salary_min': 110000,
        'salary_max': 160000,
        'location': 'San Francisco, CA',
        'job_type': 'full_time',
        'experience_required': '4+ years',
        'vacancies': 1,
    },
]

for job_data in jobs_data:
    deadline = timezone.now() + timedelta(days=30)
    Job.objects.create(
        employer=employer,
        application_deadline=deadline,
        is_active=True,
        **job_data
    )
    print(f"✓ Created job: {job_data['title']}")

print("\n✅ Sample data created successfully!")
print("\nLogin credentials:")
print("Job Seeker:")
print("  Email: jobseeker@example.com")
print("  Password: password123")
print("\nEmployer:")
print("  Email: employer@example.com")
print("  Password: password123")
