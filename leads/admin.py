from django.contrib import admin
from .models import (
    Lead, Message, Qualification,
    FollowUpConfig, FollowUpState,
    EscalationEvent
)

admin.site.register(Lead)
admin.site.register(Message)
admin.site.register(Qualification)
admin.site.register(FollowUpConfig)
admin.site.register(FollowUpState)
admin.site.register(EscalationEvent)

