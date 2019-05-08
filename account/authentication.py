from django.contrib.auth.models import User
from account.models import Profile
from django.contrib.auth.backends import AllowAllUsersModelBackend


class EmailAuthBackend(AllowAllUsersModelBackend):
    """
    Authenticate using an e-mail address.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.has_usable_password():
                if user.check_password(password):
                    return user
                else:
                    return None
            else:
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

