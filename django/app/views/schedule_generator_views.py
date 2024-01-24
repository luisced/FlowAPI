from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..utils.schedule_generator_utils import create_compatible_schedules
from ..serializers.class_loader_serializers import ScheduleSerializer


@api_view(['POST'])
def generate_schedule(request):
    courses = request.data['courses']
    compatible_schedules = create_compatible_schedules(courses)
    return Response(compatible_schedules)
