from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from news.models import News
from django.contrib.auth import get_user_model
from django.utils.text import slugify


class NewsTests(APITestCase):
    def setUp(self):
        news_data = {
                "title": "Some test",
                "sub_title": "Something bla bla ....",
                "body": "Body",
                "views": 0,
                "slug":"",
                "cover": None
            }
        User = get_user_model()
        
        user = User.objects.create_user(username='customer', password='123')
        admin = User.objects.create_superuser(username='admin', password='123')

        self.client = APIClient()
        self.news_data = news_data
        self.user = user
        self.admin = admin

    def test_get_null_news(self):
        response = self.client.get(reverse('news-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_get_news(self):
        News.objects.create(**self.news_data)
        response = self.client.get(reverse('news-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_create_news_without_authentication(self):
        url = reverse('news-list')
        response = self.client.post(url, self.news_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_with_simple_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('news-list')
        response = self.client.post(url, self.news_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_with_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('news-list')
        response = self.client.post(url, self.news_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_slug_field(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('news-list')
        response = self.client.post(url, self.news_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['slug'], slugify(self.news_data['title']))