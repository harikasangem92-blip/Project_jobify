from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, JobSeekerProfile, EmployerProfile, Job, JobApplication, ContactMessage
from django.core.exceptions import ValidationError
from django.utils import timezone


class CustomUserCreationForm(UserCreationForm):
    """
    Form for user registration
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email


class JobSeekerRegistrationForm(CustomUserCreationForm):
    """
    Registration form specifically for job seekers
    """
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number'
        })
    )
    skills = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your skills (comma-separated)',
            'rows': 3
        })
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'job_seeker'
        user.username = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
            # Create job seeker profile
            JobSeekerProfile.objects.create(
                user=user,
                skills=self.cleaned_data.get('skills', '')
            )
        return user


class EmployerRegistrationForm(CustomUserCreationForm):
    """
    Registration form specifically for employers
    """
    company_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Company Name'
        })
    )
    company_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describe your company',
            'rows': 4
        })
    )
    company_website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://yourcompany.com'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'employer'
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
            # Create employer profile
            EmployerProfile.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                company_description=self.cleaned_data.get('company_description', ''),
                company_website=self.cleaned_data.get('company_website', '')
            )
        return user


class CustomUserChangeForm(UserChangeForm):
    """
    Form for editing user profile
    """
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        if 'phone' in self.fields:
            self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        if 'profile_picture' in self.fields:
            self.fields['profile_picture'].widget.attrs.update({'class': 'form-control'})


class JobSeekerProfileForm(forms.ModelForm):
    """
    Form for job seeker profile management
    """
    class Meta:
        model = JobSeekerProfile
        fields = ('resume', 'skills', 'bio', 'experience_years', 'location')
        widgets = {
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter skills separated by commas',
                'rows': 3
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Brief bio',
                'rows': 4
            }),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your location'
            })
        }


class EmployerProfileForm(forms.ModelForm):
    """
    Form for employer profile management
    """
    class Meta:
        model = EmployerProfile
        fields = ('company_name', 'company_logo', 'company_description', 'company_website', 'company_size', 'location')
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_logo': forms.FileInput(attrs={'class': 'form-control'}),
            'company_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'company_website': forms.URLInput(attrs={'class': 'form-control'}),
            'company_size': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'})
        }


class JobForm(forms.ModelForm):
    """
    Form for creating and editing job postings
    """
    class Meta:
        model = Job
        fields = ('title', 'description', 'required_skills', 'salary_min', 'salary_max', 
                  'location', 'job_type', 'experience_required', 'application_deadline', 'vacancies')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Job Description',
                'rows': 6
            }),
            'required_skills': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Required skills (comma-separated)',
                'rows': 3
            }),
            'salary_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 300000 (3 Lakhs)',
                'min': '0',
                'max': '100000000',
                'step': '1000',
            }),
            'salary_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 550000 (5.5 Lakhs)',
                'min': '0',
                'max': '100000000',
                'step': '1000',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job Location'
            }),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'experience_required': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2 years, Entry-level'
            }),
            'application_deadline': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'vacancies': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            })
        }

    def clean_application_deadline(self):
        deadline = self.cleaned_data.get('application_deadline')
        if deadline and deadline <= timezone.now():
            raise ValidationError("Application deadline must be in the future.")
        return deadline


class JobApplicationForm(forms.ModelForm):
    """
    Form for applying to jobs
    """
    resume = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx'
        }),
        help_text='Upload your resume (PDF, DOC, DOCX). Leave blank to use the one on your profile.'
    )

    class Meta:
        model = JobApplication
        fields = ('cover_letter',)
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your cover letter here (optional)',
                'rows': 6
            })
        }


class JobSearchForm(forms.Form):
    """
    Form for searching and filtering jobs
    """
    keyword = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by job title or skill'
        })
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Location'
        })
    )
    job_type = forms.MultipleChoiceField(
        required=False,
        choices=Job.JOB_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        })
    )
    salary_min = forms.DecimalField(
        required=False,
        min_value=0,
        max_value=100000000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Salary (e.g. 300000)',
            'min': '0',
            'max': '100000000',
            'step': '1000',
        })
    )
    salary_max = forms.DecimalField(
        required=False,
        min_value=0,
        max_value=100000000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Salary (e.g. 550000)',
            'min': '0',
            'max': '100000000',
            'step': '1000',
        })
    )


class ContactForm(forms.ModelForm):
    """
    Form for contact messages
    """
    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'subject', 'message')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Message',
                'rows': 6
            })
        }
