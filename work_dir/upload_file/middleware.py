from django.shortcuts import redirect
from django.urls import reverse


class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for the home URL ('/').
        if request.path == '/':
            # Redirect to the desired URL.
            admin_url = reverse('admin:index')  # 'admin:index' is the URL name for the admin dashboard.
            return redirect(admin_url)

        response = self.get_response(request)
        return response
