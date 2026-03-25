from django.urls import path
from .views import WhatsAppConnectedView, whatsapp_webhook, StartWhatsAppSessionView, QRCodeView

urlpatterns = [
    path("webhook/", whatsapp_webhook),
    path("start/", StartWhatsAppSessionView.as_view()),
    path("connected/", WhatsAppConnectedView.as_view()),
    path("qr/", QRCodeView.as_view()),
]

