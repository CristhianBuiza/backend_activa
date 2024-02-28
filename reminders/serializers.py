from .models import Reminder
from rest_framework import serializers

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'
    
    def create(self, validated_data):
        return Reminder.objects.create(**validated_data)
    