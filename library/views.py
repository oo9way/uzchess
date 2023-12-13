from library import models, serializers, permissions
from rest_framework import generics


class BookListAPIView(generics.ListAPIView):
    serializer_class = serializers.BookListSerializer
    queryset = models.Book.objects.all()


class BookCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.BookListSerializer
    queryset = models.Book.objects.all()
    permission_classes = [permissions.IsAdminUser]


class BookDetailAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.BookDetailSerializer
    queryset = models.Book.objects.all()


class BookUpdateAPIView(generics.UpdateAPIView):
    serializer_class = serializers.BookListSerializer
    queryset = models.Book.objects.all()
    permission_classes = [permissions.IsAdminUser]


class BookDeleteAPIView(generics.DestroyAPIView):
    serializer_class = serializers.BookListSerializer
    queryset = models.Book.objects.all()
    permission_classes = [permissions.IsAdminUser]