from django.contrib import admin

from library.models import Cart, Book, Order, OrderItem

# Register your models here.


admin.site.register([Book, Cart, OrderItem, Order])
