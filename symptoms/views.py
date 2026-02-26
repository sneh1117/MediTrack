from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count, Max
from datetime import date, timedelta
from django.core.cache import cache
from .models import Symptom,Moodlog
from .serializers import SymptomSerializer, SymptomSummarySerializer,MoodLogSerializer
from accounts.permissions import IsOwnerOrDoctor
from .ai_service import HealthInsightsAI
from rest_framework.permissions import IsAuthenticated

class SymptomViewSet(viewsets.ModelViewSet):
    serializer_class = SymptomSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrDoctor]
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
    
    @action(detail=False, methods=['get'])
    def ai_insights(self, request):
        """Get AI-powered health insights"""
        user = request.user
        days = int(request.query_params.get('days', 7))
        
        # Cache key unique to user and date
        cache_key = f"ai_insights_{user.id}_{date.today()}"
        
        # Check cache first (avoid repeated API calls)
        cached_insights = cache.get(cache_key)
        if cached_insights:
            # Don't return cached errors
            if 'error' not in cached_insights:
                cached_insights['cached'] = True
                return Response(cached_insights)
            else:
                # Clear cached error and try again
                cache.delete(cache_key)
        
        # Generate new insights
        ai = HealthInsightsAI()
        insights = ai.analyze_symptoms(user, days)
        
        # Only cache successful responses (not errors)
        if 'error' not in insights:
            cache.set(cache_key, insights, 60 * 60 * 24)  # Cache for 24 hours
        
        insights['cached'] = False
        
        return Response(insights)
    
class MoodLogViewSet(viewsets.ModelViewSet):
    serializer_class=MoodLogSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Moodlog.objects.filter(user=self.request.user)
    
    @action(detail=False,methods=['get'])
    def trends(self,request):
        """Get mood trends formatted for Chart.js"""
        days = int(request.query_params.get('days',30))
        start_date=date.today()-timedelta(days=days)

        moods=self.get_queryset().filter(
            date__gte=start_date
        ).order_by('date')

        return Response({
            "labels":[m.date.strftime('%Y-%m-%d') for m in moods],
            "datasets":[{
                "label":"Mood",
                "data":[m.mood for m in moods],
                "borderColor":"rgb(153,102,255)",
                "tension":0.1
            }]
        })