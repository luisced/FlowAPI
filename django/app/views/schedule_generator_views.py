from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..utils.schedule_generator_utils import create_compatible_schedules
from ..serializers.class_loader_serializers import ScheduleGroupsListSerializer


@api_view(['POST'])
def generate_schedule(request):
    courses_data = request.data['courses']
    minimum = request.data['minimum']
    compatible_schedules = create_compatible_schedules(
        courses_data, minimum=minimum)

    generate_schedules = [{f"schedule": courses}
                          for courses in compatible_schedules]

    serializer = ScheduleGroupsListSerializer(
        data={'generated_schedules': generate_schedules})
    if serializer.is_valid():
        # If valid, return the serialized data, print the number of schedules generated
        return Response({"data": serializer.data, "count": len(generate_schedules)}, status=200)
    else:
        # If invalid, return the errors
        return Response(serializer.errors, status=400)
