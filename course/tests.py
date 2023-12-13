from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from course import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
from course.serializers import CourseCategorySerializer
from django.contrib.auth.models import User


class CourseTests(APITestCase):
    def setUp(self):


        User = get_user_model()
        
        user = User.objects.create_user(username='customer', password='123')
        admin = User.objects.create_superuser(username='admin', password='123')
        category = models.CourseCategory.objects.create(title='Test Category')
        self.category = category


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
            "category": self.category.pk,
            "language": "uz",
            "rating": "0.0"
        }
        
        def create_course():
            course_data.update({"category":category})
            obj = models.Course.objects.create(**course_data)
            course_data.update({"category":category.pk})
            return obj
        
        def create_comment(course, user):
            course_comment.update({"user":user, "course":course})
            obj = models.CourseComment.objects.create(**course_comment)
            return obj
        
        def create_lesson(course):
            course_lesson.update({"course":course})
            obj = models.CourseLesson.objects.create(**course_lesson)
            return obj
        
        self.user = user
        self.course = course_data
        self.course_category = course_category
        self.course_lesson = course_lesson
        self.course_comment = course_comment
        self.course_subscription = course_subscription
        self.admin = admin
        self.user = user
        self.create_course = create_course
        self.create_comment = create_comment
        self.create_lesson = create_lesson

    def test_get_null_course(self):
        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_with_data_course(self):
        course_data = {
            "title": "Test 1",
            "author": "TEst author ",
            "price": 0,
            "description": "Yeah",
            "category": self.category,
            "language": "uz",
            "rating": "0.0"
        }


        models.Course.objects.create(**course_data)
        response = self.client.get(reverse('course-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_create_course(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(reverse('course-create'), data=self.course)
        
        self.assertEqual(response.status_code, 201)

    def test_create_without_authentication(self):
        response = self.client.post(reverse('course-create'), data=self.course)
        
        self.assertEqual(response.status_code, 403)

    def test_create_with_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse('course-create'), data=self.course)
        
        self.assertEqual(response.status_code, 403)
        

    def test_course_details(self):
        self.client.force_authenticate(self.admin) 
        course = self.create_course()
         
        response = self.client.get(reverse('course-details', kwargs={"slug":course.slug}))
        self.assertEqual(response.status_code, 200)

    def test_update_course(self):
        self.client.force_authenticate(self.admin)
        course = self.create_course()
        
        course_data = {
            "title": "Test 1 updated",
            "author": "aouhdsuiasd",
            "price": 0,
            "description": "Yeah",
            "category": self.category.pk,
            "language": "uz",
            "rating": "0.0"
        }

        response = self.client.patch(reverse('update-course', kwargs={"slug":course.slug}), data=course_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], course_data["title"])

    def test_update_without_authentication_or_user(self):
        course = self.create_course()

        course_data = {
            "title": "Test 1 updated",
            "author": "aouhdsuiasd",
            "price": 0,
            "description": "Yeah",
            "category": self.category.pk,
            "language": "uz",
            "rating": "0.0"
        }

        response = self.client.patch(reverse('update-course', kwargs={"slug":course.slug}), data=course_data)
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(self.user)
        response = self.client.patch(reverse('update-course', kwargs={"slug":course.slug}), data=course_data)
        
        self.assertEqual(response.status_code, 403)

    def test_delete_course(self):
        self.client.force_authenticate(self.admin)
        course = self.create_course()
        
        response = self.client.delete(reverse('delete-course', kwargs={"slug":course.slug}))
        self.assertEqual(response.status_code, 204)

    def test_delete_course_without_auth_or_user(self):
        course = self.create_course()

        response = self.client.delete(reverse('delete-course', kwargs={"slug":course.slug}))
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(self.user)
        response = self.client.delete(reverse('delete-course', kwargs={"slug":course.slug}))
        
        self.assertEqual(response.status_code, 403)

    def test_create_comment(self):
        self.client.force_authenticate(self.user)
        course = self.create_course()
        
        response = self.client.post(reverse('create-comment'), data=self.course_comment)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['body'], self.course_comment['body'])

    def test_create_with_unauth(self):
        course = self.create_course()

        response = self.client.post(reverse('create-comment'), data=self.course_comment)
        self.assertEqual(response.status_code, 403)

    def test_create_comment_with_user(self):
        self.client.force_authenticate(self.user)
        course = self.create_course()
        
        response = self.client.post(reverse('create-comment'), data=self.course_comment)
        self.assertEqual(response.status_code, 201)

    def test_update_comment(self):
        self.client.force_authenticate(self.admin)
        course = self.create_course()
        comment = self.create_comment(course, self.admin)

        new_comment = {
            "body": "updated",
            "rating": 0.0
        }

        response = self.client.patch(reverse('update-comment', kwargs={"pk":comment.pk}), data=new_comment)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['body'], new_comment['body'])

    def test_update_comment_different_owner(self):
        self.client.force_authenticate(self.admin)
        course = self.create_course()
        comment = self.create_comment(course, self.user)

        new_comment = {
            "body": "updated",
            "rating": 0.0
        }

        response = self.client.patch(reverse('update-comment', kwargs={"pk":comment.pk}), data=new_comment)
        
        self.assertEqual(response.status_code, 403)

    def test_update_comment_unautherized(self):
        course = self.create_course()
        comment = self.create_comment(course, self.admin)

        new_comment = {
            "body": "updated",
            "rating": 0.0
        }

        response = self.client.patch(reverse('update-comment', kwargs={"pk":comment.pk}), data=new_comment)
        
        self.assertEqual(response.status_code, 403)

    def test_delete_comment(self):
        self.client.force_authenticate(self.admin)
        course = self.create_course()
        comment = self.create_comment(course, self.admin)

        response = self.client.delete(reverse('delete-comment', kwargs={"pk":comment.pk}))
        self.assertEqual(response.status_code, 204)

    def test_delete_comment_different_owner(self):
        self.client.force_authenticate(self.admin)
        course = self.create_course()
        comment = self.create_comment(course, self.user)

        response = self.client.delete(reverse('delete-comment', kwargs={"pk":comment.pk}))
        
        self.assertEqual(response.status_code, 403)

    def test_delete_comment_unauthorized(self):
        course = self.create_course()
        comment = self.create_comment(course, self.admin)

        response = self.client.delete(reverse('delete-comment', kwargs={"pk":comment.pk}))
        
        self.assertEqual(response.status_code, 403)

    def test_create_lesson(self):
        self.client.force_authenticate(self.admin)
        course = self.create_course()

        response = self.client.post(reverse('create-lesson'), data=self.course_lesson)

        self.assertEqual(response.status_code, 201)

    def test_create_lesson_without_auth_or_user(self):
        course = self.create_course()
        response = self.client.post(reverse('create-lesson'), data=self.course_lesson)

        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(self.user)
        response = self.client.post(reverse('create-lesson'), data=self.course_lesson)
        self.assertEqual(response.status_code, 403)


    def test_update_lesson(self):
        course = self.create_course()
        lesson = self.create_lesson(course)

        self.client.force_authenticate(self.admin)
        
        course_lesson = {
            "course": 1,
            "title":"Updated",
            "body":"Updated body",
            "active": True
        }

        response = self.client.patch(reverse('update-lesson', kwargs={"pk":lesson.pk}), data=course_lesson)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['body'], course_lesson['body'])

    def test_update_lesson_with_user_or_unauthenticated(self):
        course = self.create_course()
        lesson = self.create_lesson(course)
        
        course_lesson = {
            "course": 1,
            "title":"Updated",
            "body":"Updated body",
            "active": True
        }

        response = self.client.patch(reverse('update-lesson', kwargs={"pk":lesson.pk}), data=course_lesson)
        self.assertEqual(response.status_code, 403)


        self.client.force_authenticate(self.user)
        response = self.client.patch(reverse('update-lesson', kwargs={"pk":lesson.pk}), data=course_lesson)
        self.assertEqual(response.status_code, 403)