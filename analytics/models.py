from django.db import models
from users.models import CustomUser
from courses.models import Course  

class APIRequestLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    endpoint = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} requested {self.endpoint} at {self.timestamp}"

class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_requests = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} with {self.total_requests} requests"



class CourseActivity(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    total_views = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.course.title} with {self.total_views} views"