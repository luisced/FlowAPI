from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from ..models.user_models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is write-only
        }

    def create(self, validated_data):
        # Hash the user's password before saving
        validated_data['password'] = make_password(
            validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        # Hash the new password before saving, if it's being updated
        if validated_data.get('password'):
            validated_data['password'] = make_password(
                validated_data.get('password'))
        return super(UserSerializer, self).update(instance, validated_data)
