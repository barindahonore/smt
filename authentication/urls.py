from django.urls import path, reverse_lazy

from .views import *

urlpatterns = [
    path('', login_view, name='user_login'),
    path('accounts/login/', login_view, name='login'),
#     path('register/', register_member, name='register'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path("changepassword/", auth_views.PasswordChangeView.as_view(template_name='auth/password_reset_view.html'),
         name="set-password"),
    path("changepassworddone/",
         auth_views.PasswordChangeDoneView.as_view(template_name='auth/passwordchangedone.html'),
         name="password_change_done"),
    path('accounts/reset/<uidb64>/<token>/set-password/',
         auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html', success_url = reverse_lazy("password_reset_done")),
         name='password_reset_confirmed'),

    path('accounts/password-reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/',
         UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/',
         UserPasswordResetConfirmView.as_view(), name='password_reset_confirm_view'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='auth/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_complete.html'
    ), name='password_reset_complete'),
]
