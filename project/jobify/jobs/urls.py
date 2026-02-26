from django.urls import path
from . import views

urlpatterns = [
    # Home and Authentication
    path('', views.home, name='home'),
    path('register/choice/', views.register_choice, name='register_choice'),
    path('register/job-seeker/', views.job_seeker_register, name='job_seeker_register'),
    path('register/employer/', views.employer_register, name='employer_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Job Listings
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    
    # Job Seeker Dashboard
    path('dashboard/job-seeker/', views.job_seeker_dashboard, name='job_seeker_dashboard'),
    path('dashboard/job-seeker/profile/edit/', views.job_seeker_profile_edit, name='job_seeker_profile_edit'),
    path('jobs/<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('applications/<int:pk>/withdraw/', views.withdraw_application, name='withdraw_application'),
    
    # Employer Dashboard
    path('dashboard/employer/', views.employer_dashboard, name='employer_dashboard'),
    path('dashboard/employer/profile/edit/', views.employer_profile_edit, name='employer_profile_edit'),
    path('post-job/', views.post_job, name='post_job'),
    path('jobs/<int:pk>/edit/', views.edit_job, name='edit_job'),
    path('jobs/<int:pk>/delete/', views.delete_job, name='delete_job'),
    path('jobs/<int:pk>/applicants/', views.job_applicants, name='job_applicants'),
    path('applications/<int:pk>/update-status/', views.update_application_status, name='update_application_status'),
    
    # Contact
    path('contact/', views.contact, name='contact'),
]
