from rest_framework import serializers
from .models import Medication
from datetime import date

class MedicationSerializer(serializers.ModelSerializer):
       user = serializers.HiddenField(default=serializers.CurrentUserDefault())
       is_current = serializers.SerializerMethodField()
       
       class Meta:
           model = Medication
           fields = '__all__'
           read_only_fields = ['created_at', 'updated_at']
       
       def get_is_current(self, obj):
           today = date.today()
           if obj.end_date:
               return obj.start_date <= today <= obj.end_date
           return obj.start_date <= today
       
       def validate(self, data):
           if data.get('end_date') and data.get('start_date'):
               if data['end_date'] < data['start_date']:
                   raise serializers.ValidationError("End date must be after start date")
           
           if data.get('frequency') == 'custom' and not data.get('custom_schedule'):
               raise serializers.ValidationError("Custom schedule is required for custom frequency")
           
           return data