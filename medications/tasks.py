from celery import shared_task
from django.utils import timezone
from django.db import models
from .models import Medication, MedicationReminder
from django.core.mail import send_mail
from django.conf import settings
from datetime import time


@shared_task
def send_medication_reminders():
    now = timezone.now()
    current_hour = now.hour
    current_time = time(hour=current_hour)

    medications = Medication.objects.filter(
        is_active=True,
        start_date__lte=now.date()
    ).filter(
        models.Q(end_date__isnull=True) | models.Q(end_date__gte=now.date())
    ).select_related('user')

    reminders_sent = 0

    for med in medications:
        should_remind = False

        if med.frequency == 'once_daily' and current_hour == 8: # TEST MODE: remove current_hour =8  Always remind if active
            should_remind = True
        elif med.frequency == 'twice_daily' and current_hour in [8, 20]:
            should_remind = True
        elif med.frequency == 'three_times_daily' and current_hour in [8, 14, 20]:
            should_remind = True
        elif med.frequency == 'custom' and med.custom_schedule:
            for time_str in med.custom_schedule:
                hour = int(time_str.split(':')[0])
                if current_hour == hour:
                    should_remind = True
                    break

        if should_remind:
            # 🔥 This is calling the second task
            send_reminder_notification.delay(med.id)

            MedicationReminder.objects.create(
                medication=med,
                scheduled_time=current_time
            )

            reminders_sent += 1

    return f"Sent {reminders_sent} medication reminders"


@shared_task
def send_reminder_notification(medication_id):
    try:
        medication = Medication.objects.get(id=medication_id)
        user = medication.user

        subject = f"Medication Reminder: {medication.name}"
        message = f"""
Hi {user.username},

This is a reminder to take your medication:

Medication: {medication.name}
Dosage: {medication.dosage}

Stay healthy!
- MediTrack
        """

        if user.email:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )

        return f"Reminder sent to {user.username}"

    except Medication.DoesNotExist:
        return f"Medication {medication_id} not found"