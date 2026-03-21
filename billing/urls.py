from django.urls import path
from .views import PaymentWebhook, PlanList

urlpatterns = [
    path("payment/", PaymentWebhook.as_view()),
    path("plans/", PlanList.as_view()),
]
