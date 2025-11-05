from django.contrib.auth import logout

class ForceLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip logout for login page and login POST requests
        if request.path.startswith('/admin/login/'):
            response = self.get_response(request)
            return response
        # Logout the user on every other request to force login every time the site is accessed
        if request.user.is_authenticated:
            logout(request)
        response = self.get_response(request)
        return response
