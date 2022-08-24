"""
All Account Custom model are implimented in this file
"""
from rest_framework.authtoken.models import Token
from phonenumber_field.modelfields import PhoneNumberField

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom User Model
    """
    email = models.EmailField(_('email address'), unique=True)
    phone_number = PhoneNumberField(_('phone number'), unique=True)

    REQUIRED_FIELDS = ['email', 'phone_number']


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Pre Save user, Assign a Token to user before registration
    """
    if created:
        Token.objects.create(user=instance)
