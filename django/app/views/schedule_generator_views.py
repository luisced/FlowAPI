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

    # Genera los horarios compatibles
    generated_schedules = [{"schedule": courses}
                           for courses in compatible_schedules]

    # Preparar los datos para el serializador
    data_for_serializer = {'schedule_groups': generated_schedules}

    # Serializar los datos
    serializer = ScheduleGroupsListSerializer(data=data_for_serializer)
    if serializer.is_valid():
        # Si es válido, devuelve los datos serializados y la cantidad de horarios generados
        return Response(serializer.data)
    else:
        # Si es inválido, devuelve los errores
        return Response(serializer.errors, status=400)
