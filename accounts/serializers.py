from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
       password = serializers.CharField(write_only=True)
       
       class Meta:
           model = User
           fields = ['id', 'username', 'email', 'password', 'role', 'phone', 'date_of_birth']
       
       def create(self, validated_data):
           user = User.objects.create_user(**validated_data)
           return user

class UserSerializer(serializers.ModelSerializer):
       class Meta:
           model = User
           fields = ['id', 'username', 'email', 'role', 'phone', 'date_of_birth']