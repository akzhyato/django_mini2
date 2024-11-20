import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Enrollment

logger = logging.getLogger('courses')

@receiver(post_save, sender=Enrollment)
def log_course_enrollment(sender, instance, created, **kwargs):
    if created:
        student_email = getattr(instance.student.user, 'email', 'Unknown Email')    
        course_name = instance.course.name
        date_enrolled = instance.date_enrolled
        logger.info(f"Student {student_email} enrolled in course {course_name} on {date_enrolled}")
