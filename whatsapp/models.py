from django.db import models
from django.conf import settings
from core.models import Tenant


class WhatsAppSession(models.Model):
    STATUS = (
        ("disconnected", "Disconnected"),
        ("connecting", "Connecting"),
        ("connected", "Connected"),
    )

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    session_id = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS, default="disconnected")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.phone_number}"
