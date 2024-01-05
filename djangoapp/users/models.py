from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
# Assuming BaseModel is in a file called base/models.py
from .models import BaseModel, ActiveManager


class User(AbstractUser, BaseModel):

    active_objects = ActiveManager()

    def __str__(self):
        return self.username

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
