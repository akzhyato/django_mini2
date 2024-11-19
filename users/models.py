from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    REAL_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin')
    )
    role = models.CharField(max_length=20,
                            choices=REAL_CHOICES,
                            default='student')
    email = models.EmailField()
