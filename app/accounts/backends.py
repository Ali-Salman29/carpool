"""
Custom Backend Implimentations
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class EmailAndPhoneBackend(ModelBackend):
    """
    Email Backend, to authenticate user using email and password
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        override implimentation to email
        """
        try:
            user = User.objects.get(Q(email__iexact=username) | Q(phone_number__iexact=username))
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            pass

        return None
