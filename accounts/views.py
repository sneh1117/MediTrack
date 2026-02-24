from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response   
from .serializers import UserRegistrationSerializer, UserSerializer
from .models import User

class RegisterView(generics.CreateAPIView):
       queryset = User.objects.all()
       permission_classes = [permissions.AllowAny]
       serializer_class = UserRegistrationSerializer

class ProfileView(generics.RetrieveUpdateAPIView):
       serializer_class = UserSerializer
       permission_classes = [permissions.IsAuthenticated]
       
       def get_object(self):
           return self.request.user