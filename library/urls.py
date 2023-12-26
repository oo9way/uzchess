from django.urls import path
from library import views

urlpatterns = [
    path("books/", views.BookListAPIView.as_view(), name="books-list"),  # List of books #Tested
    path("books/create/", views.BookCreateAPIView.as_view(), name="create-book"),  # Create a new book #Tested
    path("books/<int:pk>/", views.BookDetailAPIView.as_view(), name="book-detail"),  # Book details #Tested
    path("books/update/<int:pk>/", views.BookUpdateAPIView.as_view(), name="update-book"),  # Update a book #Tested
    path("books/delete/<int:pk>/", views.BookDeleteAPIView.as_view(), name="delete-book"),  # Delete a book #Tested
]
