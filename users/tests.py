from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from attendance.models  import Attendance
from courses.models import Course
from students.models import Student
from users.models import CustomUser


class AttendanceTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.teacher = CustomUser.objects.create_user(
            username="teacher1", password="password123", role="teacher", email="teacher1@example.com"
        )
        self.student_user = CustomUser.objects.create_user(
            username="student1", password="password123", role="student", email="student1@example.com"
        )
        self.admin = CustomUser.objects.create_user(
            username="admin1", password="password123", role="admin", email="admin1@example.com"
        )

        self.student = Student.objects.create(user=self.student_user)

        self.course = Course.objects.create(
            name="Mathematics",
            description="Advanced Mathematics Course",
            instructor=self.teacher,
        )


        self.attendance = Attendance.objects.create(
            student=self.student,
            course=self.course,
            date="2024-01-01",
            status="present",
        )


        self.client.login(username="teacher1", password="password123")

    def test_list_attendance(self):

        response = self.client.get(reverse("attendance-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("results" in response.data)

    def test_create_attendance(self):

        data = {
            "student": self.student.id,
            "course": self.course.id,
            "date": "2024-02-01",
            "status": "absent",
        }
        response = self.client.post(reverse("attendance-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "absent")

    def test_update_attendance(self):

        url = reverse("attendance-detail", args=[self.attendance.id])
        data = {"status": "late"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.attendance.refresh_from_db()
        self.assertEqual(self.attendance.status, "late")

    def test_delete_attendance(self):

        url = reverse("attendance-detail", args=[self.attendance.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Attendance.objects.filter(id=self.attendance.id).exists())

    def test_student_cannot_create_attendance(self):

        self.client.login(username="student1", password="password123")
        data = {
            "student": self.student.id,
            "course": self.course.id,
            "date": "2024-02-01",
            "status": "absent",
        }
        response = self.client.post(reverse("attendance-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_attendance(self):

        self.client.login(username="admin1", password="password123")
        response = self.client.get(reverse("attendance-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
