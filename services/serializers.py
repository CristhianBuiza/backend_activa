from rest_framework import serializers
from .models import PayServices, Service, TagService, TaxiService

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagService
        fields = '__all__'
class ServiceSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Service
        fields = '__all__'

class TaxiServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxiService
        fields = ['id','title', 'icon']
        
class TaxiServiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxiService
        fields = '__all__'

class PayServicesSerializer(serializers.Serializer):
    class Meta:
        model = PayServices
        fields = '__all__'