from .models import local

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set current user in thread-local storage
        local.user = getattr(request, 'user', None)
        response = self.get_response(request)
        return response
