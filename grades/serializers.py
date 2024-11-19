from rest_framework import serializers
from .models import Grade
from students.models import Student
from courses.models import Course
from users.models import CustomUser

class GradeSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        help_text="The student ID associated with this grade."
    )
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        help_text="The course ID associated with this grade."
    )
    teacher = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='teacher'),
        help_text="The teacher ID associated with this grade."
    )

    class Meta:
        model = Grade
        fields = ['id', 'student', 'course', 'grade', 'date', 'teacher']

    def create(self, validated_data):
        return Grade.objects.create(**validated_data)
