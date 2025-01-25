import os
from email.mime.image import MIMEImage
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from authentication.tokens import account_activation_token
from .forms import LoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm

from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from admin_material.forms import RegistrationForm, LoginForm
from django.contrib.auth import logout

######################################
#          Authentications           #
######################################

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import views as auth_views
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginForm

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get("username_or_email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username_or_email, password=password)

            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin:index')
                else:
                    return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username/email or password. Please try again.')
        else:
            messages.error(request, 'Error validating the form. Please try again.')

    else:
        form = LoginForm()

    return render(request, "auth/login.html", {"form": form, 'page': 'signin'})



# def register_member(request):
#     msg = None
#     success = False
#     if request.method == 'POST':
#         members_form = MemberProfileForm(request.POST)
#         if members_form.is_valid():
#             user = members_form.save(commit=False)
#             user.is_active = False
#             user.save()

#             activate_email(request, user, members_form.cleaned_data.get('email'))

#             if request.user.is_authenticated:
#                 if request.user.is_staff:
#                     return redirect('admin:index')
#                 else:
#                     return redirect('member_dashboard')
#         else:
#             messages.error(request, 'Correct the errors highlighted in red.')
#     else:
#         members_form = MemberProfileForm()
#     return render(request, 'auth/register.html', {'members_form': members_form})


def activate_email(request, user, to_email):
    current_directory = os.getcwd()
    image_file = open(current_directory + '/static/images/logo/ssc_logo_blue.png', 'rb')
    msg_image = MIMEImage(image_file.read())
    image_file.close()
    msg_image.add_header('Content-ID', '<image1>')
    htmly = get_template('auth/activate.html')
    mail_subject = "Activate Your Account"
    data = Context({
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    }).flatten()

    html_content = htmly.render(data)
    email = EmailMultiAlternatives(mail_subject, html_content, to=[user.email])
    email.attach_alternative(html_content, "text/html")
    email.attach(msg_image)
    if email.send():
        messages.success(request,
                         f'Dear {user}, please go to your email {to_email} and click the link to activate your '
                         f'account, Thanks.')
    else:
        messages.error(request, f'Problem sending an email to {to_email}, check if it is well typed, Thanks.')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,
                         'Thank you for activating your email')
        return redirect('member_dashboard')

    else:
        messages.error(request, 'Activation link is invalid')

    return redirect('/')


class User_PasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError("This email address is not associated with any account.")
        return email


class UserPasswordResetView(PasswordResetView):
    template_name = 'auth/password_reset_view.html'
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'auth/password_reset_confirm.html'
    form_class = UserSetPasswordForm


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = UserPasswordChangeForm
