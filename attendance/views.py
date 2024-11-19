from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Attendance
from .serializers import AttendanceSerializer
from users.permissions import IsAdmin, IsTeacher, IsStudent


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course__name', 'date', 'status']
    search_fields = ['student__user__email', 'course__name']
    ordering_fields = ['date', 'status']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsTeacher | IsAdmin | IsStudent]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Attendance.objects.filter(student__user=user)
        elif user.role == 'teacher':
            return Attendance.objects.filter(course__instructor=user)
        return super().get_queryset()
