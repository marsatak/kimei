# gmao/middleware.py

from django.utils import timezone
from django.contrib.auth import logout
from django.conf import settings


class SessionExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            current_datetime = timezone.now()
            last_activity = request.session.get('last_activity')

            if last_activity:
                try:
                    last_activity = timezone.datetime.fromisoformat(last_activity)
                    if timezone.is_naive(last_activity):
                        last_activity = timezone.make_aware(last_activity)

                    if (current_datetime - last_activity).days >= 1:
                        logout(request)
                except ValueError:
                    # Si la conversion échoue, on considère la session comme expirée
                    logout(request)

            request.session['last_activity'] = current_datetime.isoformat()

        response = self.get_response(request)
        return response
