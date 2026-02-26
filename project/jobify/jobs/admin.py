from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    CustomUser, JobSeekerProfile, EmployerProfile, 
    Job, JobApplication, ContactMessage
)


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Admin interface for custom user model
    """
    list_display = ('username', 'email', 'first_name', 'role', 'created_at')
    list_filter = ('role', 'created_at', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'profile_picture', 'is_verified')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role',)}),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)


@admin.register(JobSeekerProfile)
class JobSeekerProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for job seeker profiles
    """
    list_display = ('user', 'experience_years', 'location', 'updated_at')
    list_filter = ('experience_years', 'updated_at')
    search_fields = ('user__username', 'user__email', 'location')
    readonly_fields = ('updated_at',)


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for employer profiles
    """
    list_display = ('company_name', 'user', 'company_size', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'company_size', 'created_at')
    search_fields = ('company_name', 'user__email', 'location')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """
    Admin interface for job listings
    """
    list_display = ('title', 'employer_company', 'location', 'job_type', 'is_active', 'created_at')
    list_filter = ('job_type', 'is_active', 'created_at', 'location')
    search_fields = ('title', 'description', 'location', 'employer__email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Job Information', {
            'fields': ('employer', 'title', 'description', 'required_skills')
        }),
        ('Job Details', {
            'fields': ('job_type', 'location', 'experience_required', 'vacancies')
        }),
        ('Salary', {
            'fields': ('salary_min', 'salary_max')
        }),
        ('Application', {
            'fields': ('application_deadline', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def employer_company(self, obj):
        return obj.employer.employerprofile.company_name
    employer_company.short_description = 'Company'


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    """
    Admin interface for job applications
    """
    list_display = ('applicant_name', 'job_title', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('applicant__username', 'applicant__email', 'job__title')
    readonly_fields = ('applied_at', 'updated_at')
    fieldsets = (
        ('Application Details', {
            'fields': ('job', 'applicant', 'status')
        }),
        ('Cover Letter', {
            'fields': ('cover_letter',)
        }),
        ('Timestamps', {
            'fields': ('applied_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def applicant_name(self, obj):
        return f"{obj.applicant.first_name} {obj.applicant.last_name}"
    applicant_name.short_description = 'Applicant'

    def job_title(self, obj):
        return obj.job.title
    job_title.short_description = 'Job'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin interface for contact messages
    """
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
