from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import date, timedelta
from .models import Medication,MedicationReminder


class AdherenceView(APIView):
    def get(self,request):
        user=request.user
        days=int(request.query_params.get('days',30))
        start_date=date.today()-timedelta(days=days)

        total_reminders=MedicationReminder.objects.filter(
            medication__user=user,
            sent_at__date__gte=start_date
        ).count()

        taken_reminders=MedicationReminder.objects.filter(
            medication__user=user,
            sent_at__date__gte=start_date,
            was_taken=True
        ).count()

        adherence_rate=(taken_reminders/total_reminders*100) if total_reminders >0 else 0

        return Response({
            "adherence_rate":round(adherence_rate,2),
            "total_reminders":total_reminders,
            "taken_reminders":taken_reminders,
            "missed_reminders":total_reminders-taken_reminders,
        })