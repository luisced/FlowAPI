from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..models.class_loader_models import Professor
from ..serializers.user_serializers import UserSerializer

# GET all users
