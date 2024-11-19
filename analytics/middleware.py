# middleware.py
from .models import UserActivity
from django.utils.timezone import now

class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Track API requests
            user_activity, created = UserActivity.objects.get_or_create(user=request.user)
            user_activity.total_requests += 1
            user_activity.save()

        response = self.get_response(request)
        return response
