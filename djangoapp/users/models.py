from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
# Assuming BaseModel is in a file called base/models.py
from .models import BaseModel, ActiveManager


class User(AbstractUser, BaseModel):
    # Assuming email is the unique identifier
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

    # Other custom fields can be added here

    active_objects = ActiveManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
