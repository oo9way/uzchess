from rest_framework import serializers
from library.models import Book, Cart, Order, OrderItem


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
        
        
class OrderItemSerializer(serializers.ModelSerializer):
    book = BookDetailSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ("book", "qty", "price", "is_active")
        
        
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')
    
    class Meta:
        model = Order
        fields = ("name", "phone", "total_price", 
                  "total_discount", "total_coupon", 
                  "delivery_price", "status", "order_items")
        