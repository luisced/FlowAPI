from django.db import models


class ClassLoader(models.Model):
    field1 = models.CharField(max_length=200)
    field2 = models.CharField(max_length=200)
