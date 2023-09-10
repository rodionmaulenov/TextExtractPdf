from django.contrib.auth.models import Group
from django.http import HttpResponse


def user_in_group(q1, q2):
    def decorator(view_func):
        def wrapper(self, request, *args, **kwargs):
            try:
                group1 = Group.objects.get(name='user_input_text')
                group2 = Group.objects.get(name='users_upload')
            except Group.DoesNotExist:
                group1 = None
                group2 = None
            if request.user.is_superuser:
                return view_func(self, request, *args, **kwargs)
            elif request.user.groups.filter(id=group1.id).exists() and request.user.groups.filter(id=group2.id).exists():
                return view_func(self, request, *args, **kwargs)
            else:
                return HttpResponse("Unauthorized access, you don`t have correct credentials")

        return wrapper

    return decorator
