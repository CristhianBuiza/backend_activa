from rest_framework import serializers
from .models import Profile

# User
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Un usuario con este email ya existe.")
        return value

    def valid_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Un usuario con este nombre de usuario ya existe.")
        return value

    def create(self, validated_data):
        user = validated_data.pop('user', None)
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        if user is not None:
            instance.user = user

        instance.save()
        return instance
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'