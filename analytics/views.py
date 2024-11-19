# views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Course, CourseActivity, UserActivity
from django.utils.timezone import now

# View to log course activity
def view_course(request, course_id):
    course = Course.objects.get(id=course_id)

    # Increment the view count for the course
    course_activity, created = CourseActivity.objects.get_or_create(course=course)
    course_activity.total_views += 1
    course_activity.save()

    # Track user activity
    if request.user.is_authenticated:
        user_activity, created = UserActivity.objects.get_or_create(user=request.user)
        user_activity.total_requests += 1
        user_activity.save()

    return render(request, 'course_detail.html', {'course': course})

# API to get most active users
class MostActiveUsersView(APIView):
    def get(self, request):
        active_users = UserActivity.objects.order_by('-total_requests')[:10]
        data = [{'username': user.user.username, 'total_requests': user.total_requests} for user in active_users]
        return Response(data)

# API to get most popular courses
class MostPopularCoursesView(APIView):
    def get(self, request):
        popular_courses = CourseActivity.objects.order_by('-total_views')[:10]
        data = [{'course_title': course.course.title, 'total_views': course.total_views} for course in popular_courses]
        return Response(data)
