from django.urls import include
from rest_framework.routers import DefaultRouter

from django.urls import path
from .views import StudentViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)

urlpatterns =[
    path('', include(router.urls))
]