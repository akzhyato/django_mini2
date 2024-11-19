from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Grade
from .serializers import GradeSerializer
from users.permissions import IsAdmin, IsTeacher, IsStudent
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import logging

logger = logging.getLogger('grades')


class GradePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = GradePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course__name', 'grade', 'date']
    search_fields = ['student__user__email', 'course__name', 'grade']
    ordering_fields = ['date', 'grade', 'course__name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsStudent | IsTeacher | IsAdmin]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated, IsAdmin | IsTeacher]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Grade.objects.filter(student__user=user)
        elif user.role == 'teacher':
            return Grade.objects.filter(teacher=user)
        return Grade.objects.all()

    @method_decorator(cache_page(60 * 15, key_prefix='grade_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15, key_prefix='grade_detail'))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        grade = self.get_serializer().instance
        logger.info(
            f"Преподаватель {self.request.user.email} выставил оценку {grade.grade} студенту {grade.student.user.email} по курсу {grade.course.name}")
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        grade = self.get_serializer().instance
        logger.info(
            f"Преподаватель {self.request.user.email} обновил оценку студенту {grade.student.user.email} по курсу {grade.course.name} на {grade.grade}")
        return response

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        grade = self.get_serializer().instance
        logger.info(
            f"Преподаватель {self.request.user.email} частично обновил оценку студенту {grade.student.user.email} по курсу {grade.course.name} на {grade.grade}")
        return response

    def destroy(self, request, *args, **kwargs):
        grade = self.get_object()
        response = super().destroy(request, *args, **kwargs)
        logger.info(
            f"Преподаватель {self.request.user.email} удалил оценку студенту {grade.student.user.email} по курсу {grade.course.name}")
        return response
