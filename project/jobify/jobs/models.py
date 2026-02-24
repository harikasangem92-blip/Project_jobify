from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils import timezone

# Custom User Model
class CustomUser(AbstractUser):
    """
    Extended User model with role-based functionality
    """
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
    )
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='job_seeker'
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'custom_user'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# Job Seeker Profile
class JobSeekerProfile(models.Model):
    """
    Additional profile information for job seekers
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='job_seeker_profile',
        limit_choices_to={'role': 'job_seeker'}
    )
    resume = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        null=True,
        blank=True
    )
    skills = models.TextField(
        help_text="Enter skills separated by commas",
        blank=True
    )
    bio = models.TextField(
        blank=True,
        max_length=500
    )
    experience_years = models.IntegerField(default=0)
    location = models.CharField(max_length=100, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'job_seeker_profile'
        verbose_name = 'Job Seeker Profile'
        verbose_name_plural = 'Job Seeker Profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_skills_list(self):
        """Convert comma-separated skills string to list"""
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []


# Employer Profile
class EmployerProfile(models.Model):
    """
    Additional profile information for employers
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='employer_profile',
        limit_choices_to={'role': 'employer'}
    )
    company_name = models.CharField(max_length=200)
    company_logo = models.ImageField(
        upload_to='company_logos/',
        blank=True,
        null=True
    )
    company_description = models.TextField(blank=True)
    company_website = models.URLField(blank=True)
    company_size = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('1-10', '1-10 employees'),
            ('11-50', '11-50 employees'),
            ('51-200', '51-200 employees'),
            ('201-500', '201-500 employees'),
            ('501-1000', '501-1000 employees'),
            ('1000+', '1000+ employees'),
        ]
    )
    location = models.CharField(max_length=200, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employer_profile'
        verbose_name = 'Employer Profile'
        verbose_name_plural = 'Employer Profiles'

    def __str__(self):
        return self.company_name


# Job Model
class Job(models.Model):
    """
    Job listing model
    """
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
        ('contract', 'Contract'),
    )

    employer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='posted_jobs',
        limit_choices_to={'role': 'employer'}
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.TextField(
        help_text="Enter skills separated by commas"
    )
    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    location = models.CharField(max_length=200)
    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES,
        default='full_time'
    )
    experience_required = models.CharField(
        max_length=100,
        help_text="e.g., '2 years', 'Entry-level'"
    )
    application_deadline = models.DateTimeField()
    vacancies = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'job'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_active', '-created_at']),
        ]

    def __str__(self):
        return f"{self.title} at {self.employer.employerprofile.company_name}"

    @property
    def salary_range(self):
        """Return formatted salary range in Indian Rupee format"""
        def format_amount(amount, is_stipend=False):
            """Format number into K (thousands) or Lakhs"""
            amount = float(amount)
            if amount < 100000:
                # Format as K (e.g. 15000 -> 15k)
                formatted = f"{amount / 1000:g}k"
            else:
                # Format as Lakhs (e.g. 500000 -> 5 Lakhs)
                formatted = f"{amount / 100000:g} Lakhs"
                
            return f"₹{formatted}"

        is_internship = self.job_type == 'internship'
        suffix = "/month (stipend)" if is_internship else " p.a."

        if self.salary_min and self.salary_max:
            return f"{format_amount(self.salary_min, is_internship)} – {format_amount(self.salary_max, is_internship)}{suffix}"
        elif self.salary_min:
            return f"{format_amount(self.salary_min, is_internship)}+{suffix}"
        elif self.salary_max:
            return f"Up to {format_amount(self.salary_max, is_internship)}{suffix}"
        return "Stipend on request" if is_internship else "Salary on request"

    @property
    def is_deadline_passed(self):
        """Check if application deadline has passed"""
        return timezone.now() > self.application_deadline

    def get_required_skills_list(self):
        """Convert comma-separated skills string to list"""
        if self.required_skills:
            return [skill.strip() for skill in self.required_skills.split(',')]
        return []


# Job Application Model
class JobApplication(models.Model):
    """
    Model to track job applications
    """
    APPLICATION_STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    applicant = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='job_applications',
        limit_choices_to={'role': 'job_seeker'}
    )
    status = models.CharField(
        max_length=20,
        choices=APPLICATION_STATUS_CHOICES,
        default='applied'
    )
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'job_application'
        unique_together = ('job', 'applicant')
        ordering = ['-applied_at']
        indexes = [
            models.Index(fields=['job', 'status']),
            models.Index(fields=['applicant', 'status']),
        ]

    def __str__(self):
        return f"{self.applicant.username} applied for {self.job.title}"


# Contact Message Model
class ContactMessage(models.Model):
    """
    Model to store contact form submissions
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'contact_message'
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


# Viewed Job Model for Reminders
class ViewedJob(models.Model):
    """
    Model to track when a job seeker views a job detail page
    """
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='views'
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='viewed_jobs',
        limit_choices_to={'role': 'job_seeker'}
    )
    viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'viewed_job'
        unique_together = ('job', 'user')
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.user.username} viewed {self.job.title}"
