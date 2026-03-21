from django.contrib import admin
from .models import BookingConfig, BookingEvent

admin.site.register(BookingConfig)
admin.site.register(BookingEvent)

