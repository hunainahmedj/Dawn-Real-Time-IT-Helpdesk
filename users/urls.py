from django.urls import path
from django.contrib.auth import views as auth_views
from .views import profile, super_pannel, update_emails, email_settings


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('superadmin/', super_pannel, name='super-panel'),
    path('superadmin/emails', update_emails, name='update-emails'),
    path('superadmin/email-settings', email_settings, name='email-settings'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('profile/', profile, name='user-profile')
]
