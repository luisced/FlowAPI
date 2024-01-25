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


class SingleScheduleSerializer(serializers.Serializer):
    day = serializers.CharField(max_length=1)
    start_time = serializers.TimeField(format="%H:%M:%S")
    end_time = serializers.TimeField(format="%H:%M:%S")
    room_id = serializers.IntegerField()


class ScheduleDictSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    professor_id = serializers.IntegerField()
    start_date = serializers.DateField(format="%Y-%m-%d")
    end_date = serializers.DateField(format="%Y-%m-%d")
    modality = serializers.CharField(max_length=10)
    schedule = SingleScheduleSerializer(many=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        course = Course.objects.get(pk=representation['course_id'])
        professor = Professor.objects.get(pk=representation['professor_id'])
        representation['course'] = CourseSerializer(course).data
        representation['professor'] = ProfessorSerializer(professor).data

        # Procesa cada horario individual dentro del curso
        schedule_data = []
        for schedule in representation['schedule']:
            room = Room.objects.get(pk=schedule['room_id'])
            schedule['room'] = RoomSerializer(room).data
            day_display = {'L': 'Lunes', 'M': 'Martes', 'W': 'Miércoles',
                           'J': 'Jueves', 'V': 'Viernes', 'S': 'Sábado', 'D': 'Domingo'}
            schedule['day'] = day_display.get(schedule['day'], schedule['day'])
            schedule_data.append(schedule)

        representation['schedule'] = schedule_data

        return {
            'course': representation['course'],
            'professor': professor.name,
            'schedule': representation['schedule'],
            'start_date': representation['start_date'],
            'end_date': representation['end_date'],
            'modality': representation['modality']
        }


class ScheduleGroupSerializer(serializers.Serializer):
    schedule = ScheduleDictSerializer(many=True)


class ScheduleGroupsListSerializer(serializers.Serializer):
    schedule_groups = ScheduleGroupSerializer(many=True)
