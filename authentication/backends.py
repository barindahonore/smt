from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            # Check if the input is an email
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            # If the input is not an email, try to authenticate with the username
            user = UserModel.objects.filter(username=username).first()

        if user is not None and user.check_password(password):
            return user
        else:
            return None
