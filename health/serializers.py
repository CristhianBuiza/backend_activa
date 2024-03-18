
from health.models import Health
from rest_framework import serializers


class HealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Health
        fields = ['id', 'name', 'document', 'day', 'user']
        extra_kwargs = {'user': {'read_only': True}}