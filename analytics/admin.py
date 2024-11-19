# analytics/admin.py
from django.contrib import admin
from .models import CourseActivity, UserActivity

admin.site.register(CourseActivity)
admin.site.register(UserActivity)
