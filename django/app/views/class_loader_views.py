from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import QueryDict
from ..utils.class_loader_utils import process_excel_data
from ..models import Schedule

import pandas as pd


@api_view(['POST'])
def load_course_list(request):
    # Ensure the content type of the request is multipart/form-data
    if not isinstance(request.data, QueryDict) or not request.FILES:
        return Response({"error": "The content type must be multipart/form-data."}, status=400)

    # Ensure 'file' is present in request.FILES
    if 'file' not in request.FILES:
        return Response({"error": "No file provided."}, status=400)

    file_obj = request.FILES['file']

    try:
        # You may need to handle different file types differently
        if file_obj.name.endswith('.csv'):
            data = pd.read_csv(file_obj)
            print(data)
        elif file_obj.name.endswith('.xlsx'):
            data = process_excel_data(file_obj)
            print(data)
        else:
            return Response({"error": "Unsupported file format."}, status=400)

        # Process the data here, e.g., save it to your models

        return Response({"status": "success", "data": "File processed successfully."}, status=200)
    except Exception as e:
        # In a production environment, log this exception.
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
def get_schedules(request):
    schedules = Schedule.objects.all()
    return Response(schedules)
