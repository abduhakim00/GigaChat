from rest_framework import serializers
from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ["avatar", "about"]

    def create(self, validated_data):
        validated_data['user'] = self.context['user']
        return super().create(validated_data)