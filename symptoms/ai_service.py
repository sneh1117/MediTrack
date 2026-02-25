import google.generativeai as genai
from django.conf import settings
from datetime import date, timedelta
from .models import Symptom

genai.configure(api_key=settings.GEMINI_API_KEY)

class HealthInsightsAI:
    def __init__(self):
        self.model=genai.GenerativeModel('gemini-pro')

    def analyze_symptoms(self,user,days=7):
        """Analyze user symptoms from the last N days"""
        end_date =date.today()
        start_date= end_date - timedelta(days=days)

        symptoms =Symptom.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        ).select_related('user').prefetch_related('related_medications')


        if not symptoms.exists():
            return {"insight":"Not enough symptom data to analyze. Please log symptoms for atleast a few days."}
        
        #build context for AI

        symptom_data= self._format_symptoms(symptoms)
        prompt = self._build_prompt(symptom_data,user)

        try:
            response =self.model.generate_content(prompt)
            return{
                "insight":response.text,
                "analyzed_period": f"{start_date} to {end_date}",
                "symptom_count": symptoms.count()
            }
        except Exception as e:
            return {"error": f"AI analysis failed:{str(e)}"}
        
    def _format_symptoms(self,symptoms):
        """Format symptoms for AI prompt"""
        formatted=[]
        for symptom in symptoms:
            meds=",".join([m.name for m in symptom.related_medications.all()])
            formatted.append({
                "date":str(symptom.date),
                "symptom":symptom.name,
                "severity":symptom.severity,
                "notes":symptom.notes,
                "medications":meds if meds else "None"
            })
        return formatted
    
    def _build_prompt(self,symptom_data,user):
        """Build prompt for Gemini"""
        prompt =f"""You are a helath insights assistant. Analyze the following symptom data and provide:
        1. Pattern identification(recurring symptoms,severity trends)
        2. Potential medication correlations
        3. Gentle recommendations (wehen to see a doctor,lifestyle tips)
         
        IMPORTANT :You are NOT diagnosing. Provide observations and suggest medical consulations for serious concerns.
         
        User Age: {self._calculate_age(user.date_of_birth) if user.date_of_birth else 'Not provided'}
        
        Symptom Log (last 7 days):
        """
        for item in symptom_data:
            prompt+=f"\n Date:{item['date']},Symptom:{item['symptom']},Severity:{item['severity']}/10"
            if item ['medications']:
                prompt+=f", Related Medications: {item['medications']}"
            if item ['notes']:
                prompt+=f", Notes:{item['notes']}"
        prompt += "\n\nProvide insights in a friendly, supportive tone. Keep responses under 200 words"
        return prompt
    
    def _calculate_age(self,birth_date):
        if not birth_date:
            return None
        today= date.today()
        return today.year - birth_date.year -((today.month,today.day) < (birth_date.month,birth_date.day))
