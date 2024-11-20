from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from attendance.models import Attendance
from students.models import Student
from courses.models import Course
from users.models import CustomUser

class AttendanceTests(TestCase):
    def setUp(self):
        self.teacher = CustomUser.objects.create_user(
            username="teacher1", email="teacher1@example.com", password="password", role="teacher"
        )
        self.student_user = CustomUser.objects.create_user(
            username="student1", email="student1@example.com", password="password", role="student"
        )
        self.student = Student.objects.create(user=self.student_user, dob="2000-01-01")

        # Create a course
        self.course = Course.objects.create(
            name="Math 101", description="Basic Mathematics", instructor=self.teacher
        )

        # Create an attendance record
        self.attendance = Attendance.objects.create(
            student=self.student, course=self.course, date="2024-11-18", status="present"
        )

        # Set up API client
        self.client = APIClient()

    def test_list_attendance(self):
        self.client.login(username="teacher1", password="password")
        response = self.client.get("/api/attendance/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_attendance(self):
        self.client.login(username="teacher1", password="password")
        response = self.client.get(f"/api/attendance/{self.attendance.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "present")

    def test_create_attendance(self):
        self.client.login(username="teacher1", password="password")
        data = {
            "student": self.student.id,
            "course": self.course.id,
            "date": "2024-11-19",
            "status": "absent",
        }
        response = self.client.post("/api/attendance/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendance.objects.count(), 2)

    def test_update_attendance(self):
        self.client.login(username="teacher1", password="password")
        data = {"status": "late"}
        response = self.client.patch(f"/api/attendance/{self.attendance.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.attendance.refresh_from_db()
        self.assertEqual(self.attendance.status, "late")

    def test_delete_attendance(self):
        self.client.login(username="teacher1", password="password")
        response = self.client.delete(f"/api/attendance/{self.attendance.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Attendance.objects.count(), 0)
