
from django.urls import path
from ..views import schedule_generator_views as views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('generate',
         views.generate_schedule, name='generate'),

]
