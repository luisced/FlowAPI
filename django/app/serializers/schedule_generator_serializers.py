from rest_framework import serializers
from ..serializers.class_loader_serializers import ScheduleSerializer
from ..models import Schedule


# List of Schedules Serializer


class GeneratedScheduleSerializer(serializers.ListSerializer):
    child = ScheduleSerializer()

# List of Schedules Serializer
