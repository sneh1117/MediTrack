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


class PatientSerializer(serializers.ModelSerializer):
     assigned_doctor_name= serializers.CharField(source='assigned_doctor.username',read_only=True)


     class Meta:
          model =User
          fields=['id','username','email','phone','date_of_birth','assigned_doctor', 'assigned_doctor_name']


class DoctorPatientsSerializer(serializers.ModelSerializer):
     class Meta:
          model=User
          fields=['id','username','email','phone','date_of_birth']