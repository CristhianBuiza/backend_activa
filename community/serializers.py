from rest_framework import serializers
from .models import Community, TagCommunity

class TagCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TagCommunity
        fields = '__all__'
class CommunitySerializer(serializers.ModelSerializer):
    tag = TagCommunitySerializer(many=True, read_only=True)    
    class Meta:
        model = Community
        fields = '__all__'
