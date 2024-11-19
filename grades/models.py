from django.db import models

class Grade(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    grade = models.FloatField()
    date = models.DateField()
    teacher = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)

