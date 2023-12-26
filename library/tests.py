from rest_framework.test import APITestCase, APIClient
from library import models
from django.urls import reverse
from django.contrib.auth import get_user_model


class LibraryTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()

        user = User.objects.create_user(username="customer", password="123")
        admin = User.objects.create_superuser(username="admin", password="123")

        book_data = {
            "title": "Book title",
            "price": "5.00",
            "discount_price": "4.00",
            "description": "Book description",
            "level": "intermediate",
            "author": "Author name",
            "publish_date": "2020-01-01",
        }

        def create_book():
            return models.Book.objects.create(**book_data)

        self.client = APIClient()
        self.book_data = book_data
        self.create_book = create_book
        self.user = user
        self.admin = admin

    def test_book_list(self):
        self.create_book()
        response = self.client.get(reverse("books-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_book_list_null_data(self):
        response = self.client.get(reverse("books-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)

    def test_create_book(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(reverse("create-book"), self.book_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], self.book_data["title"])

    def test_create_book_without_authentication(self):
        response = self.client.post(reverse("create-book"), self.book_data)
        self.assertEqual(response.status_code, 403)

    def test_create_book_with_user(self):
        response = self.client.post(reverse("create-book"), self.book_data)
        self.assertEqual(response.status_code, 403)

    def test_update_book(self):
        book = self.create_book()
        new_book = {"title": "updated book"}

        self.client.force_authenticate(self.admin)
        response = self.client.patch(reverse("update-book", args=[book.id]), new_book)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], new_book["title"])

    def test_update_book_without_authentication(self):
        book = self.create_book()
        new_book = {"title": "updated book"}

        response = self.client.patch(reverse("update-book", args=[book.id]), new_book)
        self.assertEqual(response.status_code, 403)

    def test_update_book_with_user(self):
        self.client.force_authenticate(self.user)
        book = self.create_book()
        new_book = {"title": "updated book"}

        response = self.client.patch(reverse("update-book", args=[book.id]), new_book)
        self.assertEqual(response.status_code, 403)

    def test_delete_book(self):
        book = self.create_book()
        self.client.force_authenticate(self.admin)
        response = self.client.delete(reverse("delete-book", args=[book.id]))
        self.assertEqual(response.status_code, 204)

    def test_delete_book_with_user(self):
        self.client.force_authenticate(self.user)
        book = self.create_book()
        response = self.client.delete(reverse("delete-book", args=[book.id]))
        self.assertEqual(response.status_code, 403)

    def test_delete_book_without_authentication(self):
        book = self.create_book()
        response = self.client.delete(reverse("delete-book", args=[book.id]))
        self.assertEqual(response.status_code, 403)

    def test_book_details(self):
        book = self.create_book()
        response = self.client.get(reverse("book-detail", args=[book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], book.title)

    def test_book_details_null_data(self):
        response = self.client.get(reverse("book-detail", args=[1]))
        self.assertEqual(response.status_code, 404)
