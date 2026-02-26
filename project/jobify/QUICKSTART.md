"""
Quick Start Guide for Jobify
"""

QUICK_START = """
╔════════════════════════════════════════════════════════════════╗
║                    JOBIFY - QUICK START                        ║
╚════════════════════════════════════════════════════════════════╝

📋 INITIAL SETUP (First Time Only)
─────────────────────────────────────

1. Create and activate virtual environment:
   
   Windows:
   $ python -m venv venv
   $ venv\\Scripts\\activate
   
   macOS/Linux:
   $ python3 -m venv venv
   $ source venv/bin/activate

2. Install dependencies:
   $ pip install -r requirements.txt

3. Run migrations:
   $ python manage.py makemigrations
   $ python manage.py migrate

4. Create admin account:
   $ python manage.py createsuperuser

5. Load sample data (optional):
   $ python manage.py shell < load_sample_data.py


🚀 RUN DEVELOPMENT SERVER
─────────────────────────────────────

$ python manage.py runserver

Access the application:
   Homepage: http://localhost:8000/
   Admin:    http://localhost:8000/admin/


👤 DEMO ACCOUNTS
─────────────────────────────────────

Job Seeker:
  Email: jobseeker@example.com
  Password: password123

Employer:
  Email: employer@example.com
  Password: password123


🔗 IMPORTANT URLS
─────────────────────────────────────

Public:
  ✓ http://localhost:8000/ - Homepage
  ✓ http://localhost:8000/jobs/ - Browse Jobs
  ✓ http://localhost:8000/register/ - Register
  ✓ http://localhost:8000/login/ - Login

Admin:
  ✓ http://localhost:8000/admin/ - Admin Panel

Job Seeker:
  ✓ http://localhost:8000/dashboard/job-seeker/ - My Dashboard

Employer:
  ✓ http://localhost:8000/dashboard/employer/ - Company Dashboard
  ✓ http://localhost:8000/post-job/ - Post a Job


⚙️ HELPFUL COMMANDS
─────────────────────────────────────

$ python manage.py shell         # Django Python shell
$ python manage.py createsuperuser  # Create new admin
$ python manage.py collectstatic --noinput  # Collect static files
$ python manage.py dumpdata > backup.json   # Backup database
$ python manage.py loaddata backup.json     # Restore database
$ python manage.py flush         # Clear database


🐛 TROUBLESHOOTING
─────────────────────────────────────

Port 8000 in use?
  $ python manage.py runserver 8080

Migration issues?
  $ python manage.py migrate --fake-initial

Static files not loading?
  $ python manage.py collectstatic --clear

Reset database:
  $ rm db.sqlite3
  $ python manage.py migrate


✉️ FEATURES CHECKLIST
─────────────────────────────────────

Dashboard Features:
  ✓ User Registration (Job Seeker & Employer)
  ✓ User Login & Authentication
  ✓ Profile Management
  ✓ Resume Upload
  ✓ Job Browsing & Filtering
  ✓ Job Application
  ✓ Application Tracking
  ✓ Job Posting (Employers)
  ✓ Applicant Management
  ✓ Contact Form
  ✓ Admin Panel
  ✓ Responsive Design


📚 FILE STRUCTURE
─────────────────────────────────────

jobify/
├── jobify_project/      ← Django configuration
├── jobs/               ← Main application
│   ├── models.py       ← Database models
│   ├── views.py        ← View logic
│   ├── forms.py        ← Form definitions
│   ├── templates/      ← HTML templates
│   ├── migrations/     ← Database migrations
│   └── admin.py        ← Admin configuration
├── static/             ← CSS & JavaScript
│   ├── css/style.css
│   └── js/script.js
├── media/              ← User uploads
├── manage.py           ← Django CLI
├── requirements.txt    ← Python dependencies
└── README.md           ← Full documentation


🎯 NEXT STEPS
─────────────────────────────────────

1. Start the server
2. Create your admin account
3. Register as Job Seeker or Employer
4. Explore the platform
5. Customize styling (static/css/style.css)
6. Add your company information
7. Post jobs or apply to them
8. Manage applications


💡 DEVELOPMENT TIPS
─────────────────────────────────────

• Debug mode is ON (DEBUG=True in settings.py)
• SQLite database is perfect for development
• Bootstrap 5 is used for styling
• No external API dependencies
• All features work offline
• Great for testing and portfolio projects


📝 EDITING TEMPLATES
─────────────────────────────────────

HTML templates are in: jobs/templates/jobs/

Edit these files to customize:
  • base.html - Main layout
  • home.html - Homepage
  • job_list.html - Job listings
  • Modify CSS in static/css/style.css


🔐 SECURITY (Production)
─────────────────────────────────────

Before going to production:
  ✓ Set DEBUG = False
  ✓ Generate new SECRET_KEY
  ✓ Configure ALLOWED_HOSTS
  ✓ Use HTTPS
  ✓ Configure Email backend
  ✓ Use PostgreSQL (not SQLite)
  ✓ Set up proper logging
  ✓ Configure backups


❓ NEED HELP?
─────────────────────────────────────

Read the full README.md for detailed documentation
Check Django docs: https://docs.djangoproject.com/


═════════════════════════════════════════════════════════════════

Ready to use Jobify? 🚀

$ python manage.py runserver

Happy coding! 🎉
"""

print(QUICK_START)
