from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from course import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User


class CourseTests(APITestCase):
    def setUp(self):


        User = get_user_model()
        
        user = User.objects.create_user(username='customer', password='123')
        admin = User.objects.create_superuser(username='admin', password='123')
        category = models.CourseCategory.objects.create(title="Course Category")
        self.category_instance = category


        course_category = {
            "title": "Some test"
        }

        course_lesson = {
            "course": 1,
            "title":"Some test",
            "body":"Some test body",
            "active": True
        }

        course_comment = {
            "user": 1,
            "course": 1,
            "body": "Some test body",
            "rating": 0.0
        }

        course_subscription = {
            "user": 1,
            "course": 1,
            "active": True
        }
        
        course_data = {
            "title": "askdnaskj ndklanskl ",
            "author": "aouhdsuiasd ",
            "price": 0,
            "description": "Yeah",
            "category": self.category_instance,
            "language": "uz",
            "rating": "0.0"
        }
        
        


        self.user = user
        self.course = course_data
        self.course_category = course_category
        self.course_lesson = course_lesson
        self.course_comment = course_comment
        self.course_subscription = course_subscription
        self.admin = admin
        self.user = user

    def test_get_null_course(self):
        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_with_data_course(self):
        course = models.Course.objects.create(**self.course)
        response = self.client.get(reverse('course-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_create_course(self):
        self.client.force_authenticate(self.admin)

        response = self.client.post(reverse('course-create'), data=self.course, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)