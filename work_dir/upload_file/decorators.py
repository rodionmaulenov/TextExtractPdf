from django.contrib.auth.models import Group
from django.http import HttpResponse


def user_in_group(q1, q2):
    def decorator(view_func):
        def wrapper(self, request, *args, **kwargs):
            try:
                group1 = Group.objects.get(name='users_input_text')
                group2 = Group.objects.get(name='users_upload')
            except Group.DoesNotExist:
                group1 = None
                group2 = None
            if request.user.is_superuser:
                return view_func(self, request, *args, **kwargs)
            elif group1 and group2 and request.user.groups.filter(
                    name=group1.name).exists() and request.user.groups.filter(name=group2.name).exists():
                return view_func(self, request, *args, **kwargs)
            else:
                return HttpResponse("Unauthorized access, you don`t have correct credentials")

        return wrapper

    return decorator
