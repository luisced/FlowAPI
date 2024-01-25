from rest_framework import serializers
from ..models import Schedule, Course, Professor, Room


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'catalog_number')


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ('id', 'name')


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'room_number', 'capacity')


class ScheduleDictSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    course_id = serializers.IntegerField()
    professor_id = serializers.IntegerField()
    room_id = serializers.IntegerField()
    start_date = serializers.DateField(format="%Y-%m-%d")
    end_date = serializers.DateField(format="%Y-%m-%d")
    start_time = serializers.TimeField(format="%H:%M:%S")
    end_time = serializers.TimeField(format="%H:%M:%S")
    day = serializers.CharField(max_length=1)
    modality = serializers.CharField(max_length=10)

    # Convert modality to human-readable format
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Get the course, professor, and room objects
        course = Course.objects.get(pk=representation['course_id'])
        professor = Professor.objects.get(pk=representation['professor_id'])
        room = Room.objects.get(pk=representation['room_id'])
        day_display = {
            'L': 'Lunes',
            'M': 'Martes',
            'W': 'Miércoles',
            'J': 'Jueves',
            'V': 'Viernes',
            'S': 'Sábado',
            'D': 'Domingo',
        }
        representation['day'] = day_display.get(
            representation['day'], representation['day'])

        return {
            'id': representation['id'],
            'course': CourseSerializer(course).data,
            'professor': professor.name,
            'room': RoomSerializer(room).data,
            'start_date': representation['start_date'],
            'end_date': representation['end_date'],
            'start_time': representation['start_time'],
            'end_time': representation['end_time'],
            'day': representation['day'],
            'modality': representation['modality'],
        }

# # Serializer for handling a list of schedules


# class ScheduleListSerializer(serializers.Serializer):
#     schedules = ScheduleDictSerializer(many=True)

#     def create(self, validated_data):
#         # Custom creation logic if necessary
#         pass

#     def update(self, instance, validated_data):
#         # Custom update logic if necessary
#         pass


# Serializer for a group of schedules (e.g., a single person's possible schedule)


class ScheduleGroupSerializer(serializers.Serializer):
    schedule = ScheduleDictSerializer(many=True)


class ScheduleGroupsListSerializer(serializers.Serializer):
    generated_schedules = ScheduleGroupSerializer(many=True)
