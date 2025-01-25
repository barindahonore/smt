from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordResetForm, PasswordChangeForm
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username or Email",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "id": "password",
                "class": "form-control",
                "autocomplete": "off",
                "data-toggle": "password"
            }
        ))

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data.get("username_or_email")
        # Check if the input is an email address
        if '@' in username_or_email:
            return username_or_email
        # If not an email, assume it's a username
        return username_or_email.strip()


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Email'
    }))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError("This email address is not associated with any account.")
        return email


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Old Password'
    }), label='Old Password')
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")


# class MemberProfileForm(UserCreationForm):
#     username = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 "placeholder": "Username",
#                 "class": "form-control"
#             }
#         ))
#     password1 = forms.CharField(
#         label="Password",
#         widget=forms.PasswordInput(
#             attrs={
#                 "placeholder": "Password",
#                 "id": "password",
#                 "class": "form-control", 'autocomplete': 'off', 'data-toggle': 'password'
#             }
#         ))
#     password2 = forms.CharField(
#         label="Confirm Password",
#         widget=forms.PasswordInput(
#             attrs={
#                 "placeholder": "Password again",
#                 "id": "password",
#                 "class": "form-control", 'autocomplete': 'off', 'data-toggle': 'password'
#             }
#         ))

#     class Meta:
#         model = MemberProfile
#         fields = ['email', 'username', 'password1', 'password2']
