from functools import wraps
from django.contrib.auth import logout
from django.shortcuts import redirect


def authenticated_users(view_func):
    @wraps(view_func)
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('admin:index')
            elif request.user.is_authenticated and request.user.id != kwargs.get('user_id'):
                logout(request)  # Logout if trying to access another user's URL
                return redirect('login')  # Redirect to login page
            else:
                print("etyyyyyyyyyyyyyyyyyyyyyyyyyyy")
                return redirect('member_dashboard')

        else:
            return view_func(request, *args, **kwargs)

    return wrapper_function
