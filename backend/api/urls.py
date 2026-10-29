from django.urls import path
from . import views
from .views import (
    RegisterView, 
    family_profile_list_create, 
    family_profile_detail, 
    ai_chat_view, 
    scan_prescription_view,
    forgot_password_view,
    reset_password_confirm_view,
    setup_2fa_view,
    model_health_check
   
)


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('family-profiles/', family_profile_list_create, name='family-profile-list-create'),
    path('family-profiles/<int:pk>/', family_profile_detail, name='family-profile-detail'),
    path('ai-chat/', ai_chat_view, name='ai-chat'),
    path('scan-prescription/', scan_prescription_view, name='scan-prescription'),
    path('forgot-password/', forgot_password_view, name='forgot-password'),
    path('reset-password-confirm/', reset_password_confirm_view, name='reset-password-confirm'),
    path('models/health/', model_health_check, name='model-health-check'),

   # Correct 2FA endpoints matching views.py
    path('auth/2fa/setup/', setup_2fa_view, name='setup-2fa'),
    path('auth/2fa/verify-enable/', views.verify_and_enable_2fa_view, name='verify-enable-2fa'),
]