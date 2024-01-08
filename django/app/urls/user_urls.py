from django.urls import path
from ..views import user_views as views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('', views.get_users, name='get_users'),
    path('create', views.create_user, name='create_user'),
    path('read/<str:pk>', views.get_user, name='get_user'),
    path('update/<str:pk>', views.update_user, name='update_user'),
    path('delete/<str:pk>', views.delete_user, name='delete_user'),
]
