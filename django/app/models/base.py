from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid


class ActiveManager(models.Manager):
    def get_queryset(self):
        # Filter the queryset to only include active (non-deleted) objects
        return super().get_queryset().filter(status=BaseModel.Status.ACTIVE)


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Updated At"))
    status = models.CharField(
        max_length=10, default='active', verbose_name=_("Status"))

    class Status(models.TextChoices):
        ACTIVE = 'active', _("Active")
        DELETED = 'deleted', _("Deleted")
        ARCHIVED = 'archived', _("Archived")

    class Meta:
        abstract = True

    def delete(self):
        self.status = self.Status.DELETED
        self.save()

    def hard_delete(self):
        super(BaseModel, self).delete()

    def restore(self):
        self.status = self.Status.ACTIVE
        self.save()

    objects = models.Manager()  # Default manager
    active_objects = ActiveManager()  # Custom manager for active objects only

    def __str__(self):
        return f"{self.__class__.__name__} {self.id}"
