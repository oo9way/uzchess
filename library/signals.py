from django.db.models.signals import pre_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError

from library.models import Cart, Order, OrderItem, Book


@receiver(pre_save, sender=Cart)
def check_product_qty(sender, instance, **kwargs):
    if not Book.can_buy(product=instance.product, qty=instance.qty):
        raise ValidationError({"qty": "Insufficient quantity"})


@receiver(pre_save, sender=Order)
def change_product_qty(sender, instance, **kwargs):
    if instance.status == "accepted":
        for order_product in OrderItem.objects.filter(order=instance):
            order_product.product.count = order_product.product.count - order_product.qty
            order_product.product.save()

    if instance.status == "cancelled":
        for order_product in OrderItem.objects.filter(order=instance):
            order_product.product.count = order_product.product.count + order_product.qty
            order_product.product.save()
