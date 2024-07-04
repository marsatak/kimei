# Dans accounts/middleware.py

from django.contrib.auth import logout


class SessionValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.session_key != request.session.session_key:
                logout(request)
                return redirect('login')
        response = self.get_response(request)
        return response
