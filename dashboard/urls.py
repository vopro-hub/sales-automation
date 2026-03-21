from django.urls import path
from .views import OverviewMetrics, LeadsList, EscalationList

urlpatterns = [
    path("overview/", OverviewMetrics.as_view()),
    path("leads/", LeadsList.as_view()),
    path("escalations/", EscalationList.as_view()),
]
