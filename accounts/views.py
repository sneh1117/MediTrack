from django.shortcuts import render


from rest_framework import generics, permissions,viewsets,status
from rest_framework.response import Response   
from rest_framework.decorators import action
from .serializers import UserRegistrationSerializer, UserSerializer,PatientSerializer,DoctorPatientsSerializer
from .models import User
from .permissions import IsDoctor, IsPatient
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

from rest_framework_simplejwt.views import TokenObtainPairView


#Limit registration to 5 attempts per hour per IP
@method_decorator(ratelimit(key='ip',rate='5/h',method='POST'),name='dispatch')
class RegisterView(generics.CreateAPIView):
       queryset = User.objects.all()
       permission_classes = [permissions.AllowAny]
       serializer_class = UserRegistrationSerializer
       

@method_decorator(ratelimit(key='ip',rate='10/h',method='POST'),name='dispatch')
class LoginView(TokenObtainPairView):
      permission_classes=[permissions.AllowAny]

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



