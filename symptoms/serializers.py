from rest_framework import serializers
from .models import Symptom
from medications.serializers import MedicationSerializer
from datetime import date

class SymptomSerializer(serializers.ModelSerializer):
       user = serializers.HiddenField(default=serializers.CurrentUserDefault())
       related_medications_details = MedicationSerializer(source='related_medications', many=True, read_only=True)
       
       class Meta:
           model = Symptom
           fields = '__all__'
           read_only_fields = ['logged_at']
       
       def validate_date(self, value):
           if value > date.today():
               raise serializers.ValidationError("Cannot log symptoms in the future")
           return value
       
       def validate_severity(self, value):
           if not 1 <= value <= 10:
               raise serializers.ValidationError("Severity must be between 1 and 10")
           return value

class SymptomSummarySerializer(serializers.Serializer):
       """For aggregated symptom data"""
       symptom_name = serializers.CharField(source="name")
       avg_severity = serializers.FloatField()
       count = serializers.IntegerField()
       last_occurrence = serializers.DateField()