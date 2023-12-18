from rest_framework import serializers
from library.models import Book, Cart 


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    book_info = BookListSerializer(read_only=True, source='book')

    class Meta:
        model = Cart
        fields = "__all__"