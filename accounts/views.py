from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions,viewsets,status
from rest_framework.response import Response   
from rest_framework.decorators import action
from .serializers import UserRegistrationSerializer, UserSerializer,PatientSerializer,DoctorPatientsSerializer
from .models import User
from .permissions import IsDoctor, IsPatient


class RegisterView(generics.CreateAPIView):
       queryset = User.objects.all()
       permission_classes = [permissions.AllowAny]
       serializer_class = UserRegistrationSerializer

class ProfileView(generics.RetrieveUpdateAPIView):
       serializer_class = UserSerializer
       permission_classes = [permissions.IsAuthenticated]
       
       def get_object(self):
           return self.request.user
       
class PatientViewSet(viewsets.ReadOnlyModelViewSet):
      serializer_class= DoctorPatientsSerializer
      permission_classes= [IsDoctor]

      def get_queryset(self):
            #doctors only see thier assigned patients
            return self.request.user.assigned_patients.all()
      

class AssignDoctorView(generics.UpdateAPIView):
      serializer_class=PatientSerializer
      permission_classes=[IsPatient]

      def get_object(self):
            return self.request.user

