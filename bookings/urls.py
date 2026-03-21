from django.urls import path
from .views import booking_webhook

urlpatterns = [
    path("webhook/", booking_webhook),
]
