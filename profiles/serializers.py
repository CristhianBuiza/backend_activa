from rest_framework import serializers
from .models import Profile
from django.core.files.base import ContentFile
import base64
import uuid

# User
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, write_only=True, required=False)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'role')
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
        role = validated_data.pop('role', None)
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Profile.objects.create(user=user, role=role) 
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