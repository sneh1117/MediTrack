from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES=(
        ('patient','Patient'),
        ('doctor','Doctor'),

    )
    role =models.CharField(max_length=50,choices=ROLE_CHOICES,default='patient')
    phone =models.CharField(max_length=15,blank=True)
    date_of_birth= models.DateField(null=True,blank=True)


    def __str__(self):
        return f"{self.username} ({self.role})"
