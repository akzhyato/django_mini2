from django.db import models
from users.models import CustomUser


class Student(models.Model):
    name = models.CharField(max_length=255, default="name")
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
