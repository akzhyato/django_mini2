from rest_framework import serializers
from .models import Attendance
from students.serializers import StudentSerializer
from courses.serializers import CourseSerializer
from students.models import Student
from courses.models import Course


class AttendanceSerializer(serializers.ModelSerializer):

    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), help_text="The course ID.")
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), help_text="The student ID.")
    status = serializers.ChoiceField(choices=Attendance.STATUS_CHOICES, help_text="Attendance status.")
    date = serializers.DateField(help_text="The date of the attendance record.")

    class Meta:
        model = Attendance
        fields = '__all__'

    def create(self, validated_data):

        student = validated_data.pop('student')
        course = validated_data.pop('course')
        attendance = Attendance.objects.create(student=student, course=course, **validated_data)
        return attendance
