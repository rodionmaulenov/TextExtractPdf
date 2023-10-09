from functools import wraps
from django.http import HttpResponse


def optimized_view_decorator(group_names):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:
                # Superuser has access to all pages
                return view_func(request, *args, **kwargs)

            if request.user.is_authenticated and request.user.is_staff:
                user_groups = request.user.groups.values_list('name', flat=True)
                if all(group in user_groups for group in group_names):
                    # User is in all required groups
                    return view_func(request, *args, **kwargs)

            return HttpResponse("Unauthorized access, you don't have correct credentials", status=403)

        return wrapper

    return decorator

