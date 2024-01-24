from rest_framework import serializers
from ..models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

    def to_representation(self, instance):
        return {

            'course': instance.course.name,
            'professor': instance.professor.name,
            'room': instance.room.room_number,
            'start_date': instance.start_date,
            'end_date': instance.end_date,
            'start_time': instance.start_time,
            'end_time': instance.end_time,
            'day': instance.day,
        }
