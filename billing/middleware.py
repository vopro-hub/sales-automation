from django.utils.timezone import now
from django.http import JsonResponse


class SubscriptionRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated:
            tenant = user.tenant
            subscription = getattr(tenant, "subscription", None)

            if not subscription or not subscription.is_active():
                return JsonResponse(
                    {"error": "Subscription inactive"},
                    status=402
                )

        return self.get_response(request)
