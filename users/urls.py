from django.urls import path, re_path, include
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet


from djoser import serializers

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
urlpatterns = [
   path('', include(router.urls))

]