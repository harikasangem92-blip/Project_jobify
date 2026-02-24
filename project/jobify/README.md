# Jobify - Job Portal Website

A complete, production-ready job portal web application built with Django, featuring role-based access control, job management, and application tracking.

## 🎯 Features

### For Job Seekers
- ✅ User registration and authentication
- ✅ Complete profile management
- ✅ Resume upload (PDF, DOC, DOCX)
- ✅ Browse and search jobs with filters
- ✅ Apply for jobs
- ✅ Track application status
- ✅ View applicant history

### For Employers
- ✅ Company profile management
- ✅ Post new job listings
- ✅ Edit and delete job postings
- ✅ View applications for each job
- ✅ Shortlist/Reject candidates
- ✅ Dashboard with statistics

### Admin Features
- ✅ Django Admin Panel
- ✅ Manage users, jobs, applications
- ✅ System statistics
- ✅ Approve/Block users

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7 (Python Web Framework)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (default) / MySQL
- **Authentication**: Django's built-in authentication system
- **File Upload**: Pillow for image processing

## 📁 Project Structure

```
jobify/
├── jobify_project/           # Django project configuration
│   ├── settings.py           # Project settings
│   ├── urls.py               # URL configuration
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
├── jobs/                     # Main application
│   ├── models.py             # Database models
│   ├── views.py              # View functions
│   ├── forms.py              # Django forms
│   ├── urls.py               # App URL patterns
│   ├── admin.py              # Admin interface
│   ├── templates/            # HTML templates
│   │   └── jobs/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── job_list.html
│   │       ├── job_detail.html
│   │       ├── job_seeker_dashboard.html
│   │       ├── employer_dashboard.html
│   │       ├── post_job.html
│   │       └── more...
│   └── migrations/           # Database migrations
├── static/                   # Static files
│   ├── css/style.css
│   └── js/script.js
├── media/                    # User uploads
├── manage.py                 # Django command utility
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (venv)

### Step 1: Clone or Extract Project

```bash
cd d:\nextgen_4.0\project\jobify
```

### Step 2: Create Virtual Environment

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Create Environment File (Optional)

Create a `.env` file for sensitive data:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Step 5: Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account:
- Username: admin
- Email: admin@example.com
- Password: (enter a secure password)

### Step 7: Collect Static Files (Production)

```bash
python manage.py collectstatic --noinput
```

### Step 8: Run Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://localhost:8000**

## 📝 Default Admin Credentials

- **URL**: http://localhost:8000/admin
- **Username**: admin (set during superuser creation)
- **Password**: (set during superuser creation)

## 👥 Demo Accounts

### Job Seeker Demo
- **Email**: jobseeker@test.com
- **Password**: testpass123

### Employer Demo
- **Email**: employer@test.com
- **Password**: testpass123

*(Create these accounts through the registration page or Django shell)*

## 🔧 Configuration

### Using MySQL Instead of SQLite

Edit `jobify_project/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jobify_db',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Install MySQL driver:
```bash
pip install mysqlclient
```

### Email Configuration

Update `settings.py` for email notifications:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 📚 Main Database Models

### CustomUser
- Extended Django User model
- Fields: role, phone, profile_picture, is_verified

### JobSeekerProfile
- Linked to CustomUser (OneToOne)
- Fields: resume, skills, bio, experience_years, location

### EmployerProfile
- Linked to CustomUser (OneToOne)
- Fields: company_name, company_logo, description, website

### Job
- Fields: title, description, salary_min/max, location, job_type, deadline
- ForeignKey to employer (CustomUser)

### JobApplication
- Tracks applications from job seekers
- Fields: job, applicant, status, cover_letter
- Unique constraint: (job, applicant)

### ContactMessage
- Stores contact form submissions

## 🌐 URL Routes

### Public Routes
- `/` - Homepage
- `/jobs/` - Job listings
- `/jobs/<id>/` - Job details
- `/login/` - Login page
- `/register/choice/` - Registration choice
- `/register/job-seeker/` - Job seeker registration
- `/register/employer/` - Employer registration
- `/contact/` - Contact page

### Job Seeker Routes
- `/dashboard/job-seeker/` - Dashboard
- `/dashboard/job-seeker/profile/edit/` - Edit profile
- `/jobs/<id>/apply/` - Apply for job

### Employer Routes
- `/dashboard/employer/` - Dashboard
- `/dashboard/employer/profile/edit/` - Edit company
- `/post-job/` - Post new job
- `/jobs/<id>/edit/` - Edit job
- `/jobs/<id>/delete/` - Delete job
- `/jobs/<id>/applicants/` - View applicants
- `/applications/<id>/update-status/` - Update application status

### Admin
- `/admin/` - Django admin panel

## 🔐 Security Features

- ✅ CSRF protection on all forms
- ✅ SQL injection prevention via ORM
- ✅ XSS protection via template escaping
- ✅ Secure password hashing
- ✅ Login required decorators
- ✅ Role-based access control
- ✅ File upload validation
- ✅ HTTPS ready (configure for production)

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop (1920px and above)
- Tablet (768px to 1024px)
- Mobile (320px to 767px)

## 🐛 Troubleshooting

### Migration Issues
```bash
python manage.py migrate --fake-initial
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Database Lock Error
Delete `db.sqlite3` and run migrations again:
```bash
rm db.sqlite3
python manage.py migrate
```

### Port 8000 Already in Use
Use a different port:
```bash
python manage.py runserver 8080
```

## 🚀 Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Update `ALLOWED_HOSTS` with your domain
3. Use a production database (PostgreSQL, MySQL)
4. Configure email backend
5. Use a WSGI server (Gunicorn, uWSGI)
6. Set up reverse proxy (Nginx, Apache)
7. Enable HTTPS/SSL
8. Use environment variables for sensitive data

### Quick Production Checklist
- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` set to random value
- [ ] Database configured
- [ ] Email configured
- [ ] Static files collected
- [ ] Media files directory set up
- [ ] ALLOWED_HOSTS updated
- [ ] HTTPS enabled
- [ ] Superuser created
- [ ] Backups configured

## 📖 API Documentation

### For Developers

The application uses Django's class-based and function-based views. Main views are in `jobs/views.py`.

### Authentication Flow

1. User registers → Account created with role
2. User logs in → Session created
3. User navigated to role-specific dashboard
4. Access control via `@login_required` decorator

## 🤝 Contributing

To add new features:

1. Create a new branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## 📄 License

This project is provided as-is for educational and commercial use.

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review Django documentation: https://docs.djangoproject.com
- Visit Django community: https://www.django-rest-framework.org

## 🎉 Success!

Your Jobify job portal is now ready to use! 

### Next Steps:
1. ✅ Run the development server
2. ✅ Create admin account
3. ✅ Register as job seeker or employer
4. ✅ Post jobs or apply for them
5. ✅ Customize styling and templates as needed

---

**Made with ❤️ for the Django community**

Last Updated: February 2024
Version: 1.0.0
