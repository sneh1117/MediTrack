from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count,Avg
from datetime import date,timedelta
from .models import Symptom
from medications.models import Medication

class DashboardView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user =request.user
        days = int(request.query_params.get('days',30))
        end_date=date.today()
        start_date=end_date - timedelta(days=days)

        #Symptom severity trends

        symptom_trends =Symptom.objects.filter(
            user=user,
            date__gte=start_date
        ).values('date').annotate(
            avg_severity=Avg('severity'),
            count=Count('id')
        ).order_by('date')

        #Active medication count

        total_medications =Medication.objects.filter(
            user=user,
            is_active=True
        ).count()

        #Most common symptoms

        common_sypmtoms =Symptom.objects.filter(
            user=user,
            date__gte=start_date
        ).values('name').annotate(
            count=Count('id'),
            avg_severity=Avg('severity')
        ).order_by('-count')[:5]

        data= {
            "symptom_trends":{
                "labels":[item['date'].strftime('%Y-%m-%d') for item in symptom_trends],
                "datasets":[{
                    "label":"Average Severity",
                    "data":[float(item['avg_severity']) for item in symptom_trends],
                    "borderColor":"rgb(75,192,192)",
                    "tension":0.1

                    },{

                    "label":"Symptom Count",
                    "data":[item['count'] for item in symptom_trends],
                    "borderColor":"rgb(255,99,132)",
                    "tension":0.1
                }]
            },

            "common_symptoms":{
                "labels":[item['name']for item in common_sypmtoms],
                "datasets":[{
                    "label":"Frequency",
                    "data":[item['count'] for item in common_sypmtoms],
                    "backgroundColor":[
                        'rgba(255,99,132,0.2)',
                        'rgba(54,162,235,0.2)',
                        'rgba(255,206,86,0.2)',
                        'rgba(75,192,192,0.2)',
                        'rgba(153,102,255,0.2)',
                    ],
                }]
            },
            "stats":{
                "active_medications":total_medications,
                "total_symptoms_logged":Symptom.objects.filter(user=user).count(),
                "symptoms_last_7_days":Symptom.objects.filter(
                    user=user,
                    date__gte=date.today() -timedelta(days=7)
                ).count(),
            }
        }

        return Response(data)

