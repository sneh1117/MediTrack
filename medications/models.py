from django.db import models
from django.conf import settings


class Medication(models.Model):
    FREQUENCY_CHOICES=(
        ('once_daily','Once Daily'),
        ('twice_daily','Twice Daily'),
        ('three_times_daily','Three Times Daily'),
        ('as_needed','As Needed'),
        ('custom','Custom Schedule'),
    )

    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='medications')
    name=models.CharField(max_length=200)
    dosage=models.CharField(max_length=100)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    custom_schedule = models.JSONField(null=True, blank=True)  # e.g., ["08:00", "14:00", "20:00"]
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering =['-created_at']

    def __str__(self):
        return f"{self.name}-{self.dosage}({self.user.username})"
    

class MedicationReminder(models.Model):
       medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='reminders')
       sent_at = models.DateTimeField(auto_now_add=True)
       scheduled_time = models.TimeField()
       was_taken = models.BooleanField(default=False)
       taken_at = models.DateTimeField(null=True, blank=True)
       
       class Meta:
           ordering = ['-sent_at']
       
       def __str__(self):
           return f"{self.medication.name} reminder at {self.scheduled_time}"