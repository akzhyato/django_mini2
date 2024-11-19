from rest_framework import serializers
from .models import Course, Enrollment
from users.models import CustomUser
from students.models import Student


class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(role='teacher'))

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        return Course.objects.create(**validated_data)


class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Enrollment
        fields = '__all__'

    def create(self, validated_data):
        student = validated_data.pop('student')
        course = validated_data.pop('course')
        enrollment = Enrollment.objects.create(student=student, course=course, **validated_data)
        return enrollment
