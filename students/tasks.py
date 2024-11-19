from celery import shared_task
from .models import Student
from users.models import CustomUser

@shared_task
def create_student_task(validated_data):
    user_data = validated_data.pop('user')
    user = CustomUser.objects.create_user(**user_data)
    Student.objects.create(user=user, **validated_data)

@shared_task
def update_student_task(student_id, validated_data):
    from .models import Student
    student = Student.objects.get(id=student_id)
    user_data = validated_data.pop('user', {})
    for attr, value in user_data.items():
        setattr(student.user, attr, value)
    student.user.save()
    for attr, value in validated_data.items():
        setattr(student, attr, value)
    student.save()
