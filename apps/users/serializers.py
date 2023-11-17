from rest_framework import serializers
from .models import AuthUserExtra
from django.contrib.auth.models import User
from .models import AuthUserExtra

class AuthUserExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUserExtra
        fields = ['code', 'img']

class UserSerializer(serializers.ModelSerializer):
    auth_user_extra = AuthUserExtraSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'auth_user_extra']

    def create(self, validated_data):
        auth_user_extra_data = validated_data.pop('auth_user_extra')
        user = User.objects.create_user(**validated_data)
        AuthUserExtra.objects.create(user=user, **auth_user_extra_data)
        return user

    def update(self, instance, validated_data):
        auth_user_extra_data = validated_data.pop('auth_user_extra', None)
        self.update_or_create_auth_user_extra(instance, auth_user_extra_data)

        return super().update(instance, validated_data)

    @staticmethod
    def update_or_create_auth_user_extra(user, auth_user_extra_data):
        AuthUserExtra.objects.update_or_create(user=user, defaults=auth_user_extra_data)
