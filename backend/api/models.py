from django.db import models
from django.contrib.auth.models import User


class FamilyProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="family_profiles", null=True, blank=True)
    name = models.CharField(max_length=150)
    relation = models.CharField(max_length=100, blank=True, null=True)
    
    
    date_of_birth = models.DateField(blank=True, null=True)
    
   
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    a1c = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    
    
    bp_systolic = models.IntegerField(blank=True, null=True)
    bp_diastolic = models.IntegerField(blank=True, null=True)
    
    conditions = models.TextField(blank=True, null=True)
    
    
    deleted_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class ChatMessage(models.Model):
    profile = models.ForeignKey(FamilyProfile, on_delete=models.CASCADE, related_name='chats')
    sender = models.CharField(max_length=10)  
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.text[:30]}"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    totp_secret = models.CharField(max_length=64, blank=True, null=True)
    is_2fa_enabled = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.user.username}"



class Consent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consents')
    policy_version = models.CharField(max_length=20, default="1.0")
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return f"Consent v{self.policy_version} by {self.user.username} at {self.timestamp}"



class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    action = models.CharField(max_length=100) # e.g., "VIEW_FAMILY_PROFILE", "AI_CHAT_QUERY", "DELETE_PROFILE"
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"[{self.timestamp}] {username} - {self.action}"


class Medicine(models.Model):
    name = models.CharField(max_length=150, unique=True)
    generic_name = models.CharField(max_length=150, blank=True, null=True)
    brand_name = models.CharField(max_length=150, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} (Generic: {self.generic_name})"