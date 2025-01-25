from django.shortcuts import render, redirect
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordChangeView,
    PasswordResetConfirmView,
)
from admin_material.forms import (
    RegistrationForm,
    LoginForm,
    UserPasswordResetForm,
    UserSetPasswordForm,
    UserPasswordChangeForm,
)
from django.contrib.auth import logout

from authentication.models import CustomUser

# from .models import Child


# Create your views here.


# Pages
def index(request):
    # available_children_count = Child.objects.count()
    male_count = CustomUser.objects.filter(gender='MALE').count()
    female_count = CustomUser.objects.filter(gender='FEMALE').count()

    context = {
        # 'available_children_count': available_children_count,
        'male_count': male_count,
        'female_count': female_count,
    }

    return render(request, "pages/index.html", context)


def billing(request):
    return render(request, "pages/billing.html", {"segment": "billing"})


def tables(request):
    return render(request, "pages/tables.html", {"segment": "tables"})


def vr(request):
    return render(request, "pages/virtual-reality.html", {"segment": "vr"})


def rtl(request):
    return render(request, "pages/rtl.html", {"segment": "rtl"})


def notification(request):
    return render(request, "pages/notifications.html", {"segment": "notification"})


def profile(request):
    return render(request, "members/pages/profile.html", {"segment": "profile"})


# Authentication
class UserLoginView(LoginView):
    template_name = "auth/login.html"
    form_class = LoginForm


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Account created successfully!")
            return redirect("user_login")
        else:
            print("Register failed!")
    else:
        form = RegistrationForm()

    context = {"form": form}
    return render(request, "auth/register.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")


class UserPasswordResetView(PasswordResetView):
    template_name = "auth/password_reset_view.html"
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "auth/password_reset_confirm.html"
    form_class = UserSetPasswordForm


class UserPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    form_class = UserPasswordChangeForm
