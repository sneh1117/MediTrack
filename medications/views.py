from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from datetime import date
from .models import Medication
from .serializers import MedicationSerializer
from accounts.permissions import IsOwnerOrDoctor
from . import models
from django.db.models import Q
class MedicationViewSet(viewsets.ModelViewSet):
       serializer_class = MedicationSerializer
       permission_classes = [IsOwnerOrDoctor]
       filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
       filterset_fields = ['is_active', 'frequency']
       search_fields = ['name', 'dosage']
       ordering_fields = ['start_date', 'created_at', 'name']
       
       def get_queryset(self):
           user = self.request.user
           if user.role == 'patient':
               return Medication.objects.filter(user=user)
           elif user.role == 'doctor':
               # Doctors see medications of their assigned patients
               patient_ids = user.assigned_patients.values_list('id', flat=True)
               return Medication.objects.filter(user_id__in=patient_ids)
           return Medication.objects.none()
       
       @action(detail=False, methods=['get'])
       def current(self, request):
           """Get currently active medications"""
           today = date.today()
           queryset = self.get_queryset().filter(
               is_active=True,
               start_date__lte=today
           ).filter(
               Q(end_date__isnull=True) | Q(end_date__gte=today)
           )
           serializer = self.get_serializer(queryset, many=True)
           return Response(serializer.data)
       
       @action(detail=False, methods=['get'])
       def upcoming(self, request):
           """Get medications starting soon"""
           today = date.today()
           queryset = self.get_queryset().filter(
               start_date__gt=today
           )
           serializer = self.get_serializer(queryset, many=True)
           return Response(serializer.data)