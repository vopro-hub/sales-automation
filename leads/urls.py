from django.urls import path

from leads.views import AgentListView
from .manual_lead_capture import ManualLeadCreateView
from .api_ai_control import start_ai, pause_ai, resume_ai
from .api_assignment import assign_agent
from .api_import import import_csv

urlpatterns = [
    path("manual-create/", ManualLeadCreateView.as_view(), name="manual-leads"),
    path("<int:lead_id>/ai/start/", start_ai),
    path("<int:lead_id>/ai/pause/", pause_ai),
    path("<int:lead_id>/ai/resume/", resume_ai),
    path("<int:lead_id>/assign/", assign_agent),
    path("import/csv/", import_csv),
    path("agents/list/", AgentListView.as_view())
]



