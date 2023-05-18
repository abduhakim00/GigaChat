from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ["avatar", "about"]

    def create(self, validated_data):
        validated_data['user'] = self.context['user']
        return super().create(validated_data)
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'username']