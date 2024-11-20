import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Attendance

logger = logging.getLogger('attendance')

@receiver(post_save, sender=Attendance)
def log_attendance_marking(sender, instance, created, **kwargs):
    student_email = getattr(instance.student.user, 'email', 'Unknown Email')  
    course_name = instance.course.name
    date = instance.date
    status = instance.status

    if created:
        logger.info(f"Attendance marked: student {student_email}, course {course_name}, date {date}, status {status}")
    else:
        if 'status' in kwargs and kwargs['status'] != status:
            logger.info(f"Attendance updated: student {student_email}, course {course_name}, date {date}, status {status}")
