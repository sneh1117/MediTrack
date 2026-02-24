from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count, Max
from datetime import date, timedelta
from .models import Symptom
from .serializers import SymptomSerializer, SymptomSummarySerializer
from accounts.permissions import IsOwnerOrDoctor

class SymptomViewSet(viewsets.ModelViewSet):
       serializer_class = SymptomSerializer
       permission_classes = [IsOwnerOrDoctor]
       filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
       filterset_fields = ['name', 'severity', 'date']
       search_fields = ['name', 'notes']
       ordering_fields = ['date', 'severity', 'logged_at']
       
       def get_queryset(self):
           user = self.request.user
           if user.role == 'patient':
               return Symptom.objects.filter(user=user)
           elif user.role == 'doctor':
               patient_ids = user.assigned_patients.values_list('id', flat=True)
               return Symptom.objects.filter(user_id__in=patient_ids)
           return Symptom.objects.none()
       
       @action(detail=False, methods=['get'])
       def last_seven_days(self, request):
           """Get symptoms from last 7 days"""
           seven_days_ago = date.today() - timedelta(days=7)
           queryset = self.get_queryset().filter(date__gte=seven_days_ago)
           serializer = self.get_serializer(queryset, many=True)
           return Response(serializer.data)
       
       @action(detail=False, methods=['get'])
       def summary(self, request):
           """Get aggregated symptom summary"""
           queryset = self.get_queryset().values('name').annotate(
               avg_severity=Avg('severity'),
               count=Count('id'),
               last_occurrence=Max('date')
           )
           serializer = SymptomSummarySerializer(queryset, many=True)
           return Response(serializer.data)
       
       @action(detail=False, methods=['get'])
       def by_medication(self, request):
           """Group symptoms by related medications"""
           medication_id = request.query_params.get('medication_id')
           if medication_id:
               queryset = self.get_queryset().filter(related_medications__id=medication_id)
               serializer = self.get_serializer(queryset, many=True)
               return Response(serializer.data)
           return Response({"error": "medication_id parameter required"}, status=400)