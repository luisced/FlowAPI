from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .base import BaseModel, ActiveManager


class User(AbstractUser, BaseModel):
    """
    Custom User model that extends the default AbstractUser and includes 
    soft deletion functionality from BaseModel.
    """
    # Additional fields can go here. For example:
    # phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Use the custom manager for active user querying
    active_objects = ActiveManager()

    def __str__(self):
        # Customize this to return a string representation of the user
        return self.username

    class Meta(AbstractUser.Meta):
        # Use 'AUTH_USER_MODEL = users.User' in your settings.py to refer to this model
        swappable = 'AUTH_USER_MODEL'
