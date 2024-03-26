from rest_framework import serializers
from .models import Profile
from django.core.files.base import ContentFile
import base64
import uuid
from django.db import IntegrityError, transaction
from django.contrib.auth.models import User
import re

class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, write_only=True, required=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'role')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def validate_username(self, value):
        value_lower = value.lower()  # Convertir a minúsculas
        if len(value) < 4:
            raise serializers.ValidationError("El nombre de usuario debe tener al menos 4 caracteres.")
        if User.objects.filter(username__iexact=value_lower).exists():  # Usar iexact para ignorar mayúsculas/minúsculas
            raise serializers.ValidationError("Un usuario con este nombre de usuario ya existe.")
        return value_lower  # Devolver el valor en minúsculas
    
    def validate_first_name(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("El nombre de usuario debe tener al menos 4 caracteres.")
        if not re.match("^[A-Za-z]+(?:[ '-][A-Za-z]+)*$", value) or len(value) < 2:
            raise serializers.ValidationError("El nombre debe contener solo letras y tener más de un carácter.")
        return value
    
    def validate_last_name(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("El nombre de usuario debe tener al menos 4 caracteres.")
        if not re.match("^[A-Za-z]+(?:[ '-][A-Za-z]+)*$", value) or len(value) < 2:
            raise serializers.ValidationError("El apellido debe contener solo letras y tener más de un carácter.")
        return value
    
    def validate_email(self, value):
        value_lower = value.lower()  
        if User.objects.filter(email__iexact=value_lower).exists():  # Usar iexact para ignorar mayúsculas/minúsculas
            raise serializers.ValidationError("Un usuario con este email ya existe.")
        return value_lower  

    def valid_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Un usuario con este nombre de usuario ya existe.")
        return value

    def create(self, validated_data):
        role = validated_data.pop('role', None)
        user = None
        try:
            with transaction.atomic():
                user = super().create(validated_data)
                user.set_password(validated_data['password'])
                user.save()
                # Check if the user already has a profile to avoid IntegrityError
                profile, created = Profile.objects.get_or_create(user=user)
                if not created:
                    # Optionally update the profile's role if it already exists
                    profile.role = role
                    profile.save()
                else:
                    profile.role = role
                    profile.save()
        except IntegrityError as e:
            # Handle the unique constraint violation
            print(f"Error creating user profile: {e}")
            # Optionally, you could raise a custom validation error to be handled by the API response
            raise serializers.ValidationError("A profile for this user already exists.")

        return {'id': user.id, 'username': user.username, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name, 'role': role}
        
class UserRecognitionSerializer(serializers.ModelSerializer):
    photo_base64 = serializers.CharField(write_only=True, allow_blank=True, required=False)

    class Meta:
        model = Profile
        fields = ('user', 'photo', 'created', 'photo_base64')
        read_only_fields = ('user', 'created')

    def validate_photo_base64(self, value):
        # Opcional: validar el tamaño/formato de la imagen codificada aquí
        if value == '':
            return None
        if not value.startswith('data:image'):
            raise serializers.ValidationError("Formato de imagen inválido.")
        return value

    def update(self, instance, validated_data):
        photo_base64 = validated_data.pop('photo_base64', None)
        if photo_base64:
            # Convertir base64 a archivo de imagen
            format, imgstr = photo_base64.split(';base64,') 
            ext = format.split('/')[-1] 
            data = ContentFile(base64.b64decode(imgstr), name=f"{uuid.uuid4()}.{ext}")  # Crear un nuevo ContentFile
            instance.photo = data
        
        instance.save()
        return instance  
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'