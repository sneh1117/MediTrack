import google.generativeai as genai
from django.conf import settings
from datetime import date, timedelta
from .models import Symptom
import time

genai.configure(api_key=settings.GEMINI_API_KEY)

class HealthInsightsAI:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def analyze_symptoms(self, user, days=7):
        """Analyze user's symptoms from the last N days"""
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        symptoms = Symptom.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        ).select_related('user').prefetch_related('related_medications')
        
        if not symptoms.exists():
            return {"insight": "Not enough symptom data to analyze. Please log symptoms for at least a few days."}
        
        # MOCK AI FOR TESTING (bypasses rate limits)
        if settings.USE_MOCK_AI:
            symptom_data = self._format_symptoms(symptoms)
            
            # Generate basic insights from symptoms
            symptom_names = [s.name for s in symptoms]
            most_common = max(set(symptom_names), key=symptom_names.count) if symptom_names else "None"
            avg_severity = sum(s.severity for s in symptoms) / len(symptoms) if symptoms else 0
            
            mock_insight = f"""**[MOCK AI RESPONSE - Testing Mode]**

Based on your symptom logs over the past {days} days, here are some observations:

**Key Patterns:**
- You logged {symptoms.count()} symptoms during this period
- Most frequent symptom: {most_common} (appears {symptom_names.count(most_common)} times)
- Average severity: {avg_severity:.1f}/10
- Date range: {start_date.strftime('%B %d')} to {end_date.strftime('%B %d, %Y')}

**Observations:**
Your symptom pattern suggests you may be experiencing recurring {most_common.lower()}. The severity levels indicate this is worth monitoring closely.

**Gentle Recommendations:**
1. Continue tracking your symptoms daily for better pattern recognition
2. Note any potential triggers (stress, diet, sleep, environment)
3. Consider keeping a journal of activities that precede symptom onset
4. If symptoms persist or worsen, consult a healthcare provider

**Note:** This is a mock response for testing purposes. To enable real AI analysis, set USE_MOCK_AI=False in your .env file.

Remember: These are observations to help you track patterns, not medical diagnoses. Always consult healthcare professionals for medical advice.
"""
            
            return {
                "insight": mock_insight,
                "analyzed_period": f"{start_date} to {end_date}",
                "symptom_count": symptoms.count(),
                "mock": True,
                "cached": False
            }
        
        # REAL AI (rest of existing code)
        symptom_data = self._format_symptoms(symptoms)
        prompt = self._build_prompt(symptom_data, user)
        
        # Try with retry logic for rate limits
        max_retries = 2
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                return {
                    "insight": response.text,
                    "analyzed_period": f"{start_date} to {end_date}",
                    "symptom_count": symptoms.count()
                }
            except Exception as e:
                error_str = str(e)
                
                # Check if it's a rate limit error
                if "429" in error_str or "quota" in error_str.lower():
                    if attempt < max_retries - 1:
                        wait_time = 10
                        if "retry in" in error_str.lower():
                            try:
                                import re
                                match = re.search(r'retry in (\d+\.?\d*)s', error_str)
                                if match:
                                    wait_time = float(match.group(1)) + 1
                            except:
                                pass
                        
                        print(f"Rate limit hit. Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        return {
                            "error": "Rate limit exceeded. Please try again in a few moments.",
                            "retry_after_seconds": 10
                        }
                else:
                    return {"error": f"AI analysis failed: {error_str[:200]}"}
        
        return {"error": "Failed to generate insights after retries"}
    
    def _format_symptoms(self, symptoms):
        """Format symptoms for AI prompt"""
        formatted = []
        for symptom in symptoms:
            meds = ", ".join([m.name for m in symptom.related_medications.all()])
            formatted.append({
                "date": str(symptom.date),
                "symptom": symptom.name,
                "severity": symptom.severity,
                "notes": symptom.notes,
                "medications": meds if meds else "None"
            })
        return formatted
    
    def _build_prompt(self, symptom_data, user):
        """Build prompt for Gemini"""
        prompt = f"""You are a health insights assistant. Analyze the following symptom data and provide:
1. Pattern identification (recurring symptoms, severity trends)
2. Potential medication correlations
3. Gentle recommendations (when to see a doctor, lifestyle tips)

IMPORTANT: You are NOT diagnosing. Provide observations and suggest medical consultation for serious concerns.

User Age: {self._calculate_age(user.date_of_birth) if user.date_of_birth else 'Not provided'}

Symptom Log (last {len(symptom_data)} days):
"""
        
        for item in symptom_data:
            prompt += f"\n- Date: {item['date']}, Symptom: {item['symptom']}, Severity: {item['severity']}/10"
            if item['medications']:
                prompt += f", Related Medications: {item['medications']}"
            if item['notes']:
                prompt += f", Notes: {item['notes']}"
        
        prompt += "\n\nProvide insights in a friendly, supportive tone. Keep response under 200 words."
        return prompt
    
    def _calculate_age(self, birth_date):
        if not birth_date:
            return None
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))