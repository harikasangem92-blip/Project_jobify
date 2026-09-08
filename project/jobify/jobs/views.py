from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    CustomUser, Job, JobApplication, JobSeekerProfile, 
    EmployerProfile, ContactMessage, ViewedJob
)
from .forms import (
    JobSeekerRegistrationForm, EmployerRegistrationForm,
    JobForm, JobApplicationForm, JobSearchForm,
    JobSeekerProfileForm, EmployerProfileForm, ContactForm,
    CustomUserChangeForm, SkillGapForm, ResumeBuilderForm
)
from .models import JobRole


# ==================== Authentication Views ====================

def home(request):
    """
    Homepage view with featured jobs
    """
    featured_jobs = Job.objects.filter(
        is_active=True,
        application_deadline__gt=timezone.now()
    ).select_related('employer').order_by('-created_at')[:6]
    
    total_jobs = Job.objects.filter(is_active=True).count()
    total_companies = EmployerProfile.objects.count()
    total_applications = JobApplication.objects.count()
    
    context = {
        'featured_jobs': featured_jobs,
        'total_jobs': total_jobs,
        'total_companies': total_companies,
        'total_applications': total_applications,
    }
    return render(request, 'jobs/home.html', context)


def register_choice(request):
    """
    Page to choose registration type (Job Seeker or Employer)
    """
    return render(request, 'jobs/register_choice.html')


def job_seeker_register(request):
    """
    Job seeker registration view
    """
    if request.method == 'POST':
        form = JobSeekerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = JobSeekerRegistrationForm()
    
    context = {'form': form, 'register_type': 'Job Seeker'}
    return render(request, 'jobs/register.html', context)


def employer_register(request):
    """
    Employer registration view
    """
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = EmployerRegistrationForm()
    
    context = {'form': form, 'register_type': 'Employer'}
    return render(request, 'jobs/register.html', context)


def user_login(request):
    """
    User login view with role-based redirect
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = CustomUser.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                
                # Redirect based on role
                if user.role == 'admin':
                    return redirect('admin:index')
                elif user.role == 'employer':
                    return redirect('employer_dashboard')
                else:  # job_seeker
                    return redirect('job_seeker_dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'jobs/login.html')


@login_required(login_url='login')
def user_logout(request):
    """
    User logout view
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


# ==================== Job Listing Views ====================

def job_list(request):
    """
    Display all available jobs with search and filter functionality
    """
    jobs = Job.objects.filter(
        is_active=True,
        application_deadline__gt=timezone.now()
    ).select_related('employer').prefetch_related('applications')
    
    form = JobSearchForm(request.GET or None)
    
    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        location = form.cleaned_data.get('location')
        job_types = form.cleaned_data.get('job_type')
        salary_min = form.cleaned_data.get('salary_min')
        salary_max = form.cleaned_data.get('salary_max')
        
        if keyword:
            jobs = jobs.filter(
                Q(title__icontains=keyword) |
                Q(description__icontains=keyword) |
                Q(required_skills__icontains=keyword)
            )
        
        if location:
            jobs = jobs.filter(location__icontains=location)
        
        if job_types:
            jobs = jobs.filter(job_type__in=job_types)
        
        if salary_min:
            jobs = jobs.filter(salary_max__gte=salary_min)
        
        if salary_max:
            jobs = jobs.filter(salary_min__lte=salary_max)
    
    # Pagination
    paginator = Paginator(jobs, 10)
    page = request.GET.get('page')
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)
    
    context = {'jobs': jobs, 'form': form}
    return render(request, 'jobs/job_list.html', context)


def job_detail(request, pk):
    """
    Display detailed information about a specific job
    """
    job = get_object_or_404(
        Job.objects.select_related('employer'),
        pk=pk,
        is_active=True
    )
    
    # Check if user has already applied
    user_applied = False
    if request.user.is_authenticated and request.user.role == 'job_seeker':
        user_applied = JobApplication.objects.filter(
            job=job,
            applicant=request.user
        ).exists()
        
        # Track job view if not applied
        if not user_applied:
            ViewedJob.objects.update_or_create(
                job=job,
                user=request.user,
                defaults={'viewed_at': timezone.now()}
            )
    
    required_skills = job.get_required_skills_list()
    
    context = {
        'job': job,
        'required_skills': required_skills,
        'user_applied': user_applied,
    }
    return render(request, 'jobs/job_detail.html', context)


def skill_gap(request):
    """Compare a user's current skills with those needed for a target role."""
    form = SkillGapForm(request.POST or None)
    results = None

    if request.method == 'POST' and form.is_valid():
        current_skills = {
            skill.strip().lower()
            for skill in form.cleaned_data['skills'].split(',')
            if skill.strip()
        }
        job_role = form.cleaned_data['job_role']
        required_skills = [
            skill.strip().lower()
            for skill in job_role.required_skills.split(',')
            if skill.strip()
        ]
        matched = [skill for skill in required_skills if skill in current_skills]
        missing = [skill for skill in required_skills if skill not in current_skills]
        results = {
            'job_role': job_role,
            'matched': matched,
            'missing': missing,
            'percent': round((len(matched) / len(required_skills)) * 100) if required_skills else 0,
        }

    return render(request, 'jobs/skill_gap.html', {'form': form, 'results': results})


def learning_roadmap(request):
    """Create a phased learning plan from a user's skills and target role."""
    initial = {}
    if request.user.is_authenticated and request.user.role == 'job_seeker':
        profile = getattr(request.user, 'job_seeker_profile', None)
        if profile and profile.skills:
            initial['skills'] = profile.skills

    form = SkillGapForm(request.POST or None, initial=initial if request.method == 'GET' else None)
    roadmap = None

    if request.method == 'POST' and form.is_valid():
        current_skills = {
            skill.strip().lower()
            for skill in form.cleaned_data['skills'].split(',')
            if skill.strip()
        }
        job_role = form.cleaned_data['job_role']
        required_skills = [
            skill.strip()
            for skill in job_role.required_skills.split(',')
            if skill.strip()
        ]
        missing = [skill for skill in required_skills if skill.lower() not in current_skills]
        phase_count = max(1, min(3, len(missing)))
        phases = [missing[index::phase_count] for index in range(phase_count)]
        phase_titles = ['Foundation', 'Build and practice', 'Job-ready polish']
        phase_descriptions = [
            'Learn the core concepts and vocabulary for your target role.',
            'Build a small project that proves you can use these skills together.',
            'Turn your work into evidence with a portfolio, resume updates, and interview practice.',
        ]
        roadmap = {
            'job_role': job_role,
            'current_count': len(required_skills) - len(missing),
            'total_count': len(required_skills),
            'percent': round(((len(required_skills) - len(missing)) / len(required_skills)) * 100) if required_skills else 0,
            'phases': [
                {
                    'number': index + 1,
                    'title': phase_titles[index],
                    'description': phase_descriptions[index],
                    'skills': skills,
                }
                for index, skills in enumerate(phases)
            ],
        }

    return render(request, 'jobs/learning_roadmap.html', {'form': form, 'roadmap': roadmap})


@login_required(login_url='login')
def resume_builder(request):
    """Save and preview a structured resume for a job seeker."""
    if request.user.role != 'job_seeker':
        messages.error(request, 'Only job seekers can build a resume.')
        return redirect('home')
    profile, _ = JobSeekerProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ResumeBuilderForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resume draft saved successfully.')
            return redirect('resume_builder')
    else:
        form = ResumeBuilderForm(instance=profile)
    return render(request, 'jobs/resume_builder.html', {'form': form, 'profile': profile})


INTERVIEW_QUESTIONS = {
    'technical': [
        ('Explain a project you built and the decisions you made.', 'Use the problem, your approach, the tools, and a measurable result.'),
        ('How do you debug a problem you have not seen before?', 'Describe how you reproduce it, isolate the cause, test a fix, and document the result.'),
        ('How do you keep your technical skills current?', 'Mention a learning habit and show how you apply it in projects or work.'),
    ],
    'behavioral': [
        ('Tell me about yourself.', 'Connect your experience, strongest skills, and the role you want next.'),
        ('Tell me about a time something went wrong.', 'Use STAR: situation, task, action, result. Focus on what you learned.'),
        ('How do you handle competing priorities?', 'Explain how you clarify impact, agree on deadlines, and communicate trade-offs.'),
    ],
}


@login_required(login_url='login')
def interview_preparation(request):
    """Create role-specific interview practice prompts."""
    if request.user.role != 'job_seeker':
        messages.error(request, 'Only job seekers can use interview preparation.')
        return redirect('home')
    role_id = request.GET.get('role') or request.POST.get('role')
    selected_role = JobRole.objects.filter(pk=role_id).first() if role_id else None
    questions = []
    if selected_role:
        questions = [
            (f'Which {skill.strip()} concepts would you use in this role?', 'Explain one example from your experience or a small project.')
            for skill in selected_role.required_skills.split(',')[:4]
            if skill.strip()
        ]
    questions += INTERVIEW_QUESTIONS['technical'] + INTERVIEW_QUESTIONS['behavioral']
    return render(request, 'jobs/interview_preparation.html', {
        'roles': JobRole.objects.order_by('title'),
        'selected_role': selected_role,
        'questions': questions,
    })


# ==================== Job Seeker Dashboard Views ====================

@login_required(login_url='login')
def job_seeker_dashboard(request):
    """
    Job seeker dashboard
    """
    if request.user.role != 'job_seeker':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        profile = JobSeekerProfile.objects.get(user=request.user)
    except JobSeekerProfile.DoesNotExist:
        profile = JobSeekerProfile.objects.create(user=request.user)
    
    applications = JobApplication.objects.filter(
        applicant=request.user
    ).select_related('job').order_by('-applied_at')
    
    # Statistics
    total_applications = applications.count()
    shortlisted = applications.filter(status='shortlisted').count()
    rejected = applications.filter(status='rejected').count()
    
    # Paginate applications
    paginator = Paginator(applications, 10)
    page = request.GET.get('page')
    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        applications = paginator.page(1)
    except EmptyPage:
        applications = paginator.page(paginator.num_pages)
    
    # Job Matching Logic
    matched_jobs = []
    user_skills = profile.get_skills_list()
    
    if user_skills:
        # Build a query that checks if ANY of the user's skills are in the job's required_skills
        skill_query = Q()
        for skill in user_skills:
            # We use icontains to do a case-insensitive search for each skill in required_skills text field
            skill_query |= Q(required_skills__icontains=skill)
            
        matched_jobs = Job.objects.filter(
            is_active=True,
            application_deadline__gt=timezone.now()
        ).filter(skill_query).exclude(
            # Exclude jobs the user has already applied to
            applications__applicant=request.user
        ).select_related('employer').distinct()[:5]  # Limit to top 5 matches
        
    # Reminders Logic (Jobs viewed but not applied, ordered by closest deadline)
    reminders = Job.objects.filter(
        views__user=request.user,
        is_active=True,
        application_deadline__gt=timezone.now()
    ).exclude(
        applications__applicant=request.user
    ).order_by('application_deadline')[:5]
        
    context = {
        'profile': profile,
        'applications': applications,
        'total_applications': total_applications,
        'shortlisted': shortlisted,
        'rejected': rejected,
        'matched_jobs': matched_jobs,
        'user_skills': user_skills,
        'reminders': reminders,
    }
    return render(request, 'jobs/job_seeker_dashboard.html', context)


@login_required(login_url='login')
def application_tracker(request):
    """Show a job seeker's applications with status filters and totals."""
    if request.user.role != 'job_seeker':
        messages.error(request, 'Only job seekers can view application tracking.')
        return redirect('home')

    applications = JobApplication.objects.filter(
        applicant=request.user
    ).select_related('job', 'job__employer').order_by('-updated_at')
    status_filter = request.GET.get('status', '').strip()
    valid_statuses = dict(JobApplication.APPLICATION_STATUS_CHOICES)
    if status_filter in valid_statuses:
        applications = applications.filter(status=status_filter)
    else:
        status_filter = ''

    all_applications = JobApplication.objects.filter(applicant=request.user)
    context = {
        'applications': applications,
        'status_filter': status_filter,
        'status_choices': JobApplication.APPLICATION_STATUS_CHOICES,
        'total_applications': all_applications.count(),
        'active_applications': all_applications.exclude(status='rejected').count(),
        'shortlisted': all_applications.filter(status='shortlisted').count(),
        'accepted': all_applications.filter(status='accepted').count(),
    }
    return render(request, 'jobs/application_tracker.html', context)


@login_required(login_url='login')
def job_seeker_profile_edit(request):
    """
    Edit job seeker profile
    """
    if request.user.role != 'job_seeker':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        profile = JobSeekerProfile.objects.get(user=request.user)
    except JobSeekerProfile.DoesNotExist:
        profile = JobSeekerProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        profile_form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('job_seeker_dashboard')
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        profile_form = JobSeekerProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile
    }
    return render(request, 'jobs/job_seeker_profile_edit.html', context)


@login_required(login_url='login')
def apply_job(request, pk):
    """
    Apply for a job
    """
    if request.user.role != 'job_seeker':
        messages.error(request, 'Only job seekers can apply for jobs.')
        return redirect('home')
    
    job = get_object_or_404(Job, pk=pk, is_active=True)
    
    # Check if deadline has passed
    if job.is_deadline_passed:
        messages.error(request, 'The application deadline for this job has passed.')
        return redirect('job_detail', pk=pk)
    
    # Check if already applied
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=pk)
    
    # Get or create seeker profile (for resume display/update)
    try:
        profile = JobSeekerProfile.objects.get(user=request.user)
    except JobSeekerProfile.DoesNotExist:
        profile = JobSeekerProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # Update user info if changed during application
            user_updated = False
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')

            if first_name and first_name != request.user.first_name:
                request.user.first_name = first_name
                user_updated = True
            if last_name and last_name != request.user.last_name:
                request.user.last_name = last_name
                user_updated = True
            if email and email != request.user.email:
                request.user.email = email
                request.user.username = email  # Keep username synced with email
                user_updated = True
            if phone and phone != request.user.phone:
                request.user.phone = phone
                user_updated = True
                
            if user_updated:
                request.user.save()

            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            
            # If a new resume was uploaded, also save it to the seeker profile
            if request.FILES.get('resume'):
                profile.resume = request.FILES['resume']
                profile.save()
            elif not profile.resume:
                # If they didn't upload a resume and don't have one on profile, show warning
                # (Though they can still submit without it based on form validation, 
                # we might want to encourage it)
                pass
                
            # Send Email Confirmation
            subject = f"Application Received: {job.title}"
            
            # Safely get company name (some jobs might be posted by superusers without an EmployerProfile)
            employer_profile = getattr(job.employer, 'employerprofile', None)
            company_name = employer_profile.company_name if employer_profile else job.employer.get_full_name() or "the employer"

            message = (
                f"Dear {request.user.first_name},\n\n"
                f"Thank you for applying to the {job.title} position at "
                f"{company_name}.\n\n"
                f"Your application has been received successfully and will be reviewed by the employer. "
                f"You can track the status of your application from your Jobify dashboard.\n\n"
                f"Best regards,\nThe Jobify Team"
            )
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@jobify.com',
                    [request.user.email],
                    fail_silently=True,
                )
            except Exception as e:
                # Log error or handle gracefully if email fails (esp in dev mode)
                print(f"Error sending email: {e}")
            
            # Application successful, remove from ViewedJobs if exists so it's no longer a reminder
            ViewedJob.objects.filter(job=job, user=request.user).delete()
            
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('job_detail', pk=pk)
    else:
        form = JobApplicationForm()
    
    context = {'form': form, 'job': job, 'profile': profile}
    return render(request, 'jobs/apply_job.html', context)

@login_required(login_url='login')
def withdraw_application(request, pk):
    """
    Allow job seeker to withdraw/decline their past application
    """
    if request.user.role != 'job_seeker':
        messages.error(request, "Only job seekers can decline applications.")
        return redirect('home')
        
    application = get_object_or_404(JobApplication, pk=pk, applicant=request.user)
    
    if request.method == 'POST':
        # Delete the application so it is removed from the dashboard
        job_title = application.job.title
        application.delete()
        messages.success(request, f"You have successfully declined your application for {job_title}.")
        
    return redirect('job_seeker_dashboard')


# ==================== Employer Dashboard Views ====================

@login_required(login_url='login')
def employer_dashboard(request):
    """
    Employer dashboard
    """
    if request.user.role != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        employer_profile = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        employer_profile = EmployerProfile.objects.create(user=request.user, company_name="")
    
    posted_jobs = Job.objects.filter(employer=request.user).order_by('-created_at')
    total_jobs = posted_jobs.count()
    
    # Get total applications for all jobs
    total_applications = JobApplication.objects.filter(
        job__employer=request.user
    ).count()
    
    # Get shortlisted count
    shortlisted_applications = JobApplication.objects.filter(
        job__employer=request.user,
        status='shortlisted'
    ).count()
    
    context = {
        'employer_profile': employer_profile,
        'posted_jobs': posted_jobs,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'shortlisted_applications': shortlisted_applications,
    }
    return render(request, 'jobs/employer_dashboard.html', context)


@login_required(login_url='login')
def employer_profile_edit(request):
    """
    Edit employer profile
    """
    if request.user.role != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        employer_profile = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        employer_profile = EmployerProfile.objects.create(user=request.user, company_name="")
    
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        profile_form = EmployerProfileForm(request.POST, request.FILES, instance=employer_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('employer_dashboard')
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        profile_form = EmployerProfileForm(instance=employer_profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': employer_profile
    }
    return render(request, 'jobs/employer_profile_edit.html', context)


@login_required(login_url='login')
def post_job(request):
    """
    Post a new job (Employer only)
    """
    if request.user.role != 'employer':
        messages.error(request, 'Only employers can post jobs.')
        return redirect('home')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('employer_dashboard')
    else:
        form = JobForm()
    
    context = {'form': form}
    return render(request, 'jobs/post_job.html', context)


@login_required(login_url='login')
def edit_job(request, pk):
    """
    Edit a job posting (Employer only)
    """
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    
    if request.user.role != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('employer_dashboard')
    else:
        form = JobForm(instance=job)
    
    context = {'form': form, 'job': job}
    return render(request, 'jobs/post_job.html', context)


@login_required(login_url='login')
def delete_job(request, pk):
    """
    Delete a job posting (Employer only)
    """
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    
    if request.user.role != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('employer_dashboard')
    
    context = {'job': job}
    return render(request, 'jobs/delete_job.html', context)


@login_required(login_url='login')
def job_applicants(request, pk):
    """
    View applicants for a specific job (Employer only)
    """
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    
    if request.user.role != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    applications = JobApplication.objects.filter(job=job).select_related('applicant')
    
    # Pagination
    paginator = Paginator(applications, 10)
    page = request.GET.get('page')
    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        applications = paginator.page(1)
    except EmptyPage:
        applications = paginator.page(paginator.num_pages)
    
    context = {
        'job': job,
        'applications': applications,
    }
    return render(request, 'jobs/job_applicants.html', context)


@login_required(login_url='login')
def update_application_status(request, pk):
    """
    Update application status (Employer only)
    """
    application = get_object_or_404(JobApplication, pk=pk)
    
    if request.user.role != 'employer' or application.job.employer != request.user:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(JobApplication.APPLICATION_STATUS_CHOICES):
            application.status = status
            application.save()
            messages.success(request, f'Application status updated to {status}!')
            return redirect('job_applicants', pk=application.job.pk)
    
    context = {'application': application}
    return render(request, 'jobs/update_application_status.html', context)


# ==================== Contact View ====================

def contact(request):
    """
    Contact form view
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('home')
    else:
        form = ContactForm()
    
    context = {'form': form}
    return render(request, 'jobs/contact.html', context)
