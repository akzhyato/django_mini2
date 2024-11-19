# urls.py
from django.urls import path
from .views import MostActiveUsersView, MostPopularCoursesView

urlpatterns = [
    path('most-active-users/', MostActiveUsersView.as_view(), name='most_active_users'),
    path('most-popular-courses/', MostPopularCoursesView.as_view(), name='most_popular_courses'),
]
