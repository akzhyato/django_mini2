from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from requests import Response
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Student
from .serializers import StudentSerializer
from users.permissions import IsStudent, IsAdmin
from .tasks import update_student_task, create_student_task


class StudentViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given student.

    list:
    Return a list of all students.

    create:
    Create a new student.

    update:
    Update an existing student.

    partial_update:
    Partially update an existing student.

    destroy:
    Delete a student.
    """

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['registration_date']
    search_fields = ['user__email', 'user__username']
    ordering_fields = ['registration_date', 'user__email']

    def get_permissions(self):
        if self.action in ['retrieve', 'update']:
            permission_classes = [IsAuthenticated, IsStudent | IsAdmin]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Customize the queryset based on the user role.
        """
        user = self.request.user
        if user.role == 'student':
            return Student.objects.filter(user=user)
        return Student.objects.all()

    @method_decorator(cache_page(60 * 15, key_prefix='student_list'))
    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of all students.
        """
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15, key_prefix='student_detail'))
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single student record.
        """
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create a new student asynchronously using Celery.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Trigger Celery task for creating a student
        create_student_task.delay(serializer.validated_data)
        return Response({"detail": "Student creation task queued."}, status=202)

    def update(self, request, *args, **kwargs):
        """
        Update a student asynchronously using Celery.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # Trigger Celery task for updating a student
        update_student_task.delay(instance.id, serializer.validated_data)
        return Response({"detail": "Student update task queued."}, status=202)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a student asynchronously using Celery.
        """
        instance = self.get_object()
        # Trigger Celery task for deleting a student
        delete_student_task.delay(instance.id)
        return Response({"detail": "Student deletion task queued."}, status=202)
