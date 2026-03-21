from django.urls import path
from analytics.views import (
    AnalyticsSummaryView,
    FunnelView,
    AgentAnalyticsView,
    SLAAnalyticsView,
    AIImpactView,
)

urlpatterns = [
    path("summary/", AnalyticsSummaryView.as_view()),
    path("funnel/", FunnelView.as_view()),
    path("agents/", AgentAnalyticsView.as_view()),
    path("sla/", SLAAnalyticsView.as_view()),
    path("ai-impact/", AIImpactView.as_view()),
]
