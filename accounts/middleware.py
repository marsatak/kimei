# Dans accounts/middleware.py

from django.contrib.auth import logout
from django.shortcuts import redirect


class SessionValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            stored_session_key = request.user.session_key
            current_session_key = request.session.session_key

            if stored_session_key and stored_session_key != current_session_key:
                logout(request)
                return redirect('login')

        response = self.get_response(request)
        return response
