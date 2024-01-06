from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model
import random


def randomnumber(N):
    minimum = pow(10, N - 1)
    maximum = pow(10, N) - 1
    return random.randint(minimum, maximum)


# Base Model class
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Book(BaseModel):
    LEVELS = (
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    )

    title = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, default="0.00", max_digits=10)
    discount_price = models.DecimalField(decimal_places=2, default="0.00", max_digits=10)
    description = models.TextField(blank=True, null=True)
    cover = models.ImageField(upload_to="data/books/covers/", blank=True, null=True)
    level = models.CharField(max_length=15, choices=LEVELS, default="beginner")
    author = models.CharField(max_length=255, null=True, blank=True)
    pages_count = models.IntegerField(default=0)
    publish_date = models.DateField(null=True, blank=True)
    count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def active(self):
        if self.is_active and self.count > 0:
            return True
        return False

    def can_buy(self, qty=0):
        # get holded books count
        holded_books = (
            OrderItem.objects.filter(book=self, is_active=True).aggregate(total_qty=Sum("qty"))["total_qty"] or 0
        )

        # return result
        return self.count - holded_books >= qty and self.active()


class Order(models.Model):
    STATUS = (
        ("initial", "Initial"),
        ("payment", "Payment"),
        ("delivery", "Delivery"),
        ("completed", "Completed"),
    )

    order_number = models.CharField(max_length=10, default=randomnumber(10))

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=128)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    total_price = models.IntegerField(default=0)
    total_discount = models.IntegerField(default=0)
    total_coupon = models.IntegerField(default=0)
    delivery_price = models.IntegerField(default=0)

    status = models.CharField(max_length=16, choices=STATUS, default="initial")

    def get_total(self):
        return self.total_discount - self.total_coupon + self.delivery_price


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    is_active = models.BooleanField(default=True)


class Cart(models.Model):
    STATUS_CHOICES = (
        ("initial", "Initial"),
        ("completed", "Completed"),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    qty = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="initial")

    def update_qty(self, qty):
        can_buy = Book.can_buy(book=self.book, qty=qty)
        if can_buy:
            self.qty = qty
            self.save()
            return True
        return False

    @classmethod
    def create_order(cls, user, name, phone):
        carts = Cart.objects.filter(user=user, status="initial")
        all_available = all([Book.can_buy(cart.book, cart.qty) for cart in carts])

        if not all_available:
            return False

        order = Order.objects.create(user=user, name=name, phone=phone)

        total_price = 0
        total_discount = 0
        order_items = []

        for cart in carts:
            total_price += cart.book.price * cart.qty
            total_discount += cart.book.discount_price * cart.qty

            order_item = OrderItem(order=order, book=cart.book, price=cart.book.discount_price, qty=cart.qty)
            order_items.append(order_item)

        carts.update(status="completed")
        OrderItem.objects.bulk_create(order_items)

        order.total_price = total_price
        order.total_discount = total_discount
        order.save()
        return True
