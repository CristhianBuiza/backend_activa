from rest_framework import serializers
from .models import Service, TagService

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagService
        fields = '__all__'
class ServiceSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Service
        fields = '__all__'
