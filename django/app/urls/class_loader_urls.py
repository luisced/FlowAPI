from django.urls import path
from ..views import class_loader_views as views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('load',
         views.load_course_list, name='load_course_list'),
    path('get_schedules',
         views.get_schedules, name='get_schedules'),

]
