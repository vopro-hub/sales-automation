from django.urls import path
from .tenant_onboarding_views import TenantOnboardingView
from .api_audit import audit_logs
from .api_branding import branding
from .views import TenantSignupView, LoginView, MeView

urlpatterns = [
    path("auth/signup/<slug:tenant_slug>/", TenantSignupView.as_view(), name="tenant-signup"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/me/", MeView.as_view()),
    path("audit-logs/", audit_logs),
    path("branding/", branding),
    path("tenants/onboard/", TenantOnboardingView.as_view()),


]



