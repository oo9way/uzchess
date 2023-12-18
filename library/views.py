from library import models, serializers
from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError, NotAcceptable

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


class CartListAPIView(generics.ListAPIView):
    queryset = models.Cart.objects.select_related('book')
    serializer_class = serializers.CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query =  super().get_queryset()
        return query.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='initial')

class CartAddItemAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        book_id = self.request.data['book_id']
        qty = self.request.data['qty']

        if not (book_id and qty):
            raise NotAcceptable({'error': 'Parameters are not given'})

        book = get_object_or_404(models.Book, pk=book_id)

        if book.can_buy(qty):
            carts = models.Cart.objects.filter(user=request.user, book=book)
            if carts.exists():
                cart = carts.first()
                cart.qty = qty
                cart.save()
            else:
                cart = models.Cart.objects.create(user=request.user, book=book, qty=qty)
            
            return Response(data=serializers.CartSerializer(cart).data, status=status.HTTP_201_CREATED)
        else:
            raise ValidationError({'qty':'Insufficient quantity'})        

class CartRemoveItemAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        book_id = self.request.data['book_id']
        
        if not (book_id):
            raise NotAcceptable({'error': 'Parameters are not given'})

        book = get_object_or_404(models.Book, pk=book_id)
        
        cart_item = models.Cart.objects.filter(book=book, user=request.user)
        cart_item.delete()
        
        return Response({"message":"Cart item deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    
class CreateOrderAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        name = self.request.data['name']
        phone = self.request.data['phone']
        cart = models.Cart
        if len(cart.objects.filter(user=request.user, status='initial'))<=0:
            return Response({'message':'No products'}, status=status.HTTP_400_BAD_REQUEST)
            
        if cart.create_order(request.user, name, phone):
            return Response({"message":"Order created"}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message':'Insufficient quantity'}, status=status.HTTP_400_BAD_REQUEST)
        
        