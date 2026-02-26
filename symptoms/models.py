from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from core.validators import validate_no_html
class Symptom(models.Model):
       user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='symptoms')
       name = models.CharField(max_length=200,validators=[validate_no_html])  # e.g., "Headache", "Nausea"
       severity = models.IntegerField(
           validators=[MinValueValidator(1), MaxValueValidator(10)],
           help_text="Severity on scale of 1-10"
       )
       notes = models.TextField(blank=True,validators=[validate_no_html])
       logged_at = models.DateTimeField(auto_now_add=True)
       date = models.DateField()  # Allows backdating
       
       # Link to medications to track correlations
       related_medications = models.ManyToManyField(
           'medications.Medication', 
           blank=True,
           related_name='symptoms'
       )
       
       class Meta:
           ordering = ['-date', '-logged_at']
           indexes = [
               models.Index(fields=['user', 'date']),
               models.Index(fields=['user', 'name']),
           ]
       
       def __str__(self):
           return f"{self.name} (Severity: {self.severity}) - {self.user.username}"
       

class Moodlog(models.Model):
     MOOD_CHOICES=(
          (1,'Very Bad'),
          (2,'Bad'),
          (3,'Okay'),
          (4,'Good'),
          (5,'Very Good'),
    )
     
     user =models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='moods')
     mood=models.IntegerField(choices=MOOD_CHOICES)
     notes=models.TextField(blank=True)
     date=models.DateField()
     logged_at=models.DateTimeField(auto_now_add=True)

     class Meta:
          ordering=["-date"]
          unique_together=['user','date']#one mood log per day

     def __str__(self):
        return f"{self.user.username} -{self.get_mood_display()} on {self.date}"
    