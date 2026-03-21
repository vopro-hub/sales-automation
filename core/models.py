from multiprocessing.managers import BaseManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from core.managers import UserManager
from django.utils.text import slugify

class Tenant(models.Model):
    name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    logo_url = models.URLField(blank=True)
    primary_color = models.CharField( max_length=20, default="#2563eb")
    whatsapp_number = models.CharField(max_length=30, unique=True, null=True, blank=True)
    system_prompt = models.TextField()
    is_active = models.BooleanField(default=True)
    whatsapp_sender_name = models.CharField( max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def display_name(self):
        return self.name or self.brand_name
    

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("owner", "Owner"),
        ("manager", "Manager"),
        ("agent", "Agent"),
    )
    username = models.CharField(max_length=100) 
    staff_ID = models.CharField(max_length=20, unique=True) 
    first_name = models.CharField(max_length=100) 
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    whatsapp_number = models.CharField(max_length=30, null=True, blank=True)
    tenant = models.ForeignKey("Tenant", on_delete=models.CASCADE, related_name="users",)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD ="email"
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.tenant.slug})"



class AuditLog(models.Model):
    ACTION_CHOICES = [
        ("lead_created", "Lead Created"),
        ("lead_imported", "Lead Imported"),
        ("agent_assigned", "Agent Assigned"),
        ("ai_started", "AI Started"),
        ("ai_paused", "AI Paused"),
        ("ai_resumed", "AI Resumed"),
        ("booking_confirmed", "Booking Confirmed"),
        ("booking_cancelled", "Booking Cancelled"),
        ("escalation", "Escalation"),
        ("followup_stopped", "Follow-up Stopped"),
    ]

    tenant = models.ForeignKey("Tenant", on_delete=models.CASCADE)
    user = models.ForeignKey( "core.User", null=True, blank=True,  on_delete=models.SET_NULL)

    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    object_type = models.CharField(max_length=50)  # lead, booking, system
    object_id = models.CharField(max_length=100)

    message = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

